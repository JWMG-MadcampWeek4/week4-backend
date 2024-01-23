from io import BytesIO
import json
from flask import Flask, render_template, request, jsonify, make_response, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import os
import pymongo
import requests
from flask_pymongo import PyMongo
from pymongo import MongoClient
from src.theme import theme
from src.script import script
from src.image import image_script
import requests
import json
import urllib
from PIL import Image
import base64
from PIL import Image

load_dotenv()

CLIENT = os.environ.get("CLIENT")
openai_api_key = os.environ.get("OPENAI_API_KEY")
REST_API_KEY = os.environ.get("REST_API_KEY")

app = Flask(__name__)
CORS(app) 

client = MongoClient(CLIENT)
db = client['madcampweek4']
collection_User = db['User']

@app.route("/signup", methods=['POST'])
def signup():
    data = request.json
    user_id = data.get("id")
    password = data.get("password")
    nickname = data.get("nickname")

    if collection_User.find_one({"id": user_id}):
        # User ID already exists
        return jsonify({"success": False, "message": "User ID already exists"}), 409
    else:
        # Create new user
        collection_User.insert_one({"id": user_id, "password": password, "nickname": nickname})
        return jsonify({"success": True, "message": "User registered successfully"}), 201

@app.route("/login", methods=['POST'])
def login():
    data = request.json
    user_id = data.get("id")
    password = data.get("password")

    user = collection_User.find_one({"id": user_id})
    if user and user["password"] == password:
        # Successful login
        return jsonify({"success": True, "message": "Login successful", "id": user_id, "nickname": user["nickname"]}), 200
    else:
        # Login failed
        return jsonify({"success": False, "message": "Invalid ID or password"}), 401
    
@app.route("/signup_id", methods=['POST'])
def check_duplicate_id():
    data = request.json
    user_id = data.get("id")
    
    # Check if the ID already exists in the database
    exists = collection_User.find_one({"id": user_id}) is not None
    
    # Return the result as a boolean value
    return jsonify({"exist": exists})

@app.route("/theme", methods=['POST'])
def get_contents():
    try:
        # Extracting the theme from the request body
        data = request.json
        user_theme = data.get("theme")
        print(user_theme)

        
        recommended_themes = theme(user_theme)
        return jsonify(recommended_themes)
        # # Returning the recommended themes as a JSON response
        # return jsonify(user_theme)
        
    except Exception as e:
        # In case of any exceptions, return an error message
        return jsonify({'error': str(e)}), 500


@app.route("/script", methods=['POST'])
def get_script():
    try:
        # Extracting the theme from the request body
        data = request.json
        user_content = data.get("content")
        print(user_content)

        
        recommended_script = script(user_content)
        return jsonify(recommended_script)
        # # Returning the recommended themes as a JSON response
        # return jsonify(user_theme)
        
    except Exception as e:
        # In case of any exceptions, return an error message
        return jsonify({'error': str(e)}), 500


@app.route('/image_script', methods=['POST'])
def generate_image_script():
    try:
        user_script = request.json.get("script") 
        print(script)# Assuming the user sends a JSON object with a "user_script" field
        created_image_script = image_script(user_script)
        print(user_script) # Generate image prompts from the user's script
        
        if created_image_script:
            return jsonify({"image_script": created_image_script})
        else:
            return jsonify({"error": "Failed to generate image script from user script."}), 500
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred."}), 500


def calculate_presentation_time(script):
    # 대본에서 단어 수를 세기 위해 공백으로 분할
    words = script.split()
    
    # 단어 수 계산
    word_count = len(words)
    
    # 일반적인 발표 속도를 기준으로 발표 시간 계산 (1분당 150 단어)
    words_per_minute = 150
    presentation_time_minutes = word_count / words_per_minute
    
    # 발표 시간을 분과 초로 변환
    presentation_time_minutes = round(presentation_time_minutes, 2)
    presentation_time_seconds = int(presentation_time_minutes * 60)
    
    return presentation_time_minutes, presentation_time_seconds
@app.route('/calculate', methods=['POST'])
def calculate():
    print(1)
    try:
        # Get script data from POST request as JSON
        data = request.get_json()
        script = data.get('script')
        print(script)
        
        if script:
            # Calculate presentation time based on the script
            minutes, seconds = calculate_presentation_time(script)
            
            response_data = {
                'word_count': len(script.split()),
                'presentation_time_minutes': minutes,
                'presentation_time_seconds': seconds
            }
            
            return jsonify(response_data)
        else:
            return jsonify({'error': 'Please provide a script.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500 




# [내 애플리케이션] > [앱 키] 에서 확인한 REST API 키 값 입력


# def t2i(prompt):
#     r = requests.post(
#         'https://api.kakaobrain.com/v2/inference/karlo/t2i',
#         json = {
#             'prompt': prompt,
#             'width' : 368,
#             'height': 640,
#             "upscale" : True,
#             "scale" : 4,
#             "image_quality" : 100,
            

#         },
#         headers = {
#             'Authorization': f'KakaoAK {REST_API_KEY}',
#             'Content-Type': 'application/json'
#         }
#     )
#     # 응답 JSON 형식으로 변환
#     response = json.loads(r.content)
#     return response

# # 프롬프트에 사용할 제시어
# prompt = "beautiful korean"

# # 이미지 생성하기 REST API 호출
# response = t2i(prompt)

# # 응답의 첫 번째 이미지 생성 결과 출력하기
# result = Image.open(urllib.request.urlopen(response.get("images")[0].get("image")))
# result.show()

@app.route('/text2image', methods=['POST'])
def text_to_image():
    # Extracting the image text from the POST request
    image_text = request.json.get('image_text')

    # Ensure image_text is provided
    if not image_text:
        return jsonify({"error": "No image text provided"}), 400

    # Stability AI API setup
    engine_id = "stable-diffusion-v1-6"
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    api_key = os.getenv("STABILITY_API_KEY")

    if api_key is None:
        return jsonify({"error": "Missing Stability API key"}), 500

    # Generating the image using Stability AI
    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [{"text": image_text}],
            "cfg_scale": 7,
            "height": 1344,
            "width": 768,
            "samples": 1,
            "steps": 50,
        },
    )

    if response.status_code != 200:
        return jsonify({"error": "Error in image generation"}), 500

    # Extracting the base64 string from the response
    data = response.json()
    image_base64 = data['artifacts'][0]['base64']  # Assuming first image in the response

    # Returning the base64 string
    return jsonify({"base64": image_base64}), 200


@app.route('/list2image', methods=['POST'])
def list_to_image():
    # Extracting the list of image texts from the POST request
    image_text_list = request.json.get('image_text_list')
    print(image_text_list)

    # Ensure image_text_list is provided and is a list
    if not image_text_list or not isinstance(image_text_list, list):
        return jsonify({"error": "image_text_list must be a list of prompts"}), 400

    # Stability AI API setup
    engine_id = "stable-diffusion-v1-6"
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    api_key = os.getenv("STABILITY_API_KEY")

    if api_key is None:
        return jsonify({"error": "Missing Stability API key"}), 500

    base64_list = []  # List to hold base64 strings of generated images

    # Iterate over each text prompt and generate images
    for image_text in image_text_list:
        # Generating the image using Stability AI
        response = requests.post(
            f"{api_host}/v1/generation/{engine_id}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "text_prompts": [{"text": image_text}],
                "cfg_scale": 7,
                "height": 1344,
                "width": 768,
                "samples": 1,
                "steps": 30,
            },
        )

        if response.status_code != 200:
            return jsonify({"error": "Error in image generation for prompt: " + image_text}), 500

        # Extracting the base64 string from the response
        data = response.json()
        image_base64 = data['artifacts'][0]['base64']  # Assuming first image in the response
        base64_list.append(image_base64)

    # Returning the list of base64 strings
    return jsonify({"base64_list": base64_list}), 200
# IMAGE_DIR = '/Users/springson/Downloads'
# @app.route('/upload_base64', methods=['POST'])
# def handle_base64_images():
#     base64_list = request.json.get('base64_list')
#     if not base64_list:
#         return jsonify({"error": "No base64 list provided"}), 400

#     saved_files = []
#     for i, base64_str in enumerate(base64_list):
#         try:
#             # Assume the base64 string doesn't have the prefix
#             # Directly decode the base64 string
#             image_data = base64.b64decode(base64_str)
            
#             # Create a PIL Image instance and save the image
#             image = Image.open(BytesIO(image_data))
#             filename = f'image_{i}.png'  # Assuming PNG format; adjust if necessary
#             filepath = os.path.join(IMAGE_DIR, filename)
#             image.save(filepath)
            
#             saved_files.append(filepath)
#         except Exception as e:
#             return jsonify({"error": f"An error occurred: {e}"}), 500

#     if saved_files:
#         return send_file(saved_files[0], as_attachment=True)
#     else:
#         return jsonify({"error": "No images were saved"}), 500
if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0", port = 8080)



