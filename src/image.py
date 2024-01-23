

from dotenv import load_dotenv
from flask import jsonify
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.schema import BaseOutputParser
import os
import requests
import base64
import requests
class CommaOutputParser(BaseOutputParser):

    def parse(self,text):
        item = text.strip().split(",")
        return list(map(str.strip,item))

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")


chat = ChatOpenAI(
    temperature=0.1,
    # model="gpt-4"
)


def image_script(user_script):
    try:
        # Prepare the chat prompt template
        template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are now responsible for creating image prompts for a stable diffusion model using a provided script. Overlook any sections labeled 'scenes.' Your task is to identify and compile a list of 12 distinct images, choosing names that represent concrete objects or elements rather than abstract concepts, using only one or two words for each. These names will act as prompts for generating images and should be arranged in a comma-separated list, omitting any additional context or explanation. The script as provided will be used verbatim for the voiceover. For instance, instead of 'Scene 1 - Image 1', simply compile the list of image names like 'orbit, settelite' and so on."
        ),
        ("human", f"Based on the script '{user_script}', I need to develop image prompts for a stable diffusion model. The prompts for each image should be one or two words, reflecting tangible objects or features. Please format them as a comma-separated list.")
    ]
)

        # Execute the chain of operations: template formatting, chat model prediction, and parsing
        chain = template | chat | CommaOutputParser()
        image_script = chain.invoke({"user_script": user_script})

        # theme_list should be a list of strings if everything goes well
        print(image_script)

        # Make sure to return a serializable Python object (e.g., list or dict)
        if image_script:
            return image_script  
        else:
            raise ValueError("The returned value is not a list.")  # Raise an error if it's not a list

    except Exception as e:
        # Here you should NOT use jsonify since this function should return a Python object, not a Flask response
        # This exception will be handled by Flask's error handling in the route
        print(f"Error: {e}")
        raise e
    




#  stable-diffusion-xl-1024-v1-0
engine_id = "stable-diffusion-v1-6"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
api_key = os.getenv("STABILITY_API_KEY")

if api_key is None:
    raise Exception("Missing Stability API key.")

response = requests.post(
    f"{api_host}/v1/generation/{engine_id}/text-to-image",
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    },
    json={
        "text_prompts": [
            {
                "text": "A lighthouse on a cliff"
            }
        ],
        "cfg_scale": 7,
        "height": 1024,
        "width": 1024,
        "samples": 1,
        "steps": 30,
    },
)

if response.status_code != 200:
    raise Exception("Non-200 response: " + str(response.text))

data = response.json()




# def generate_images_with_dalle(prompts, descriptions): # Replace with your actual API key.
#     headers = {
#         'Authorization': f'Bearer {openai_api_key}',
#         'Content-Type': 'application/json'
#     }

#     image_urls_list = []

#     for i, (prompt, description) in enumerate(zip(prompts, descriptions)):
#         payload = {
#             'prompt': prompt,
#             'n': 1,  # Generate one image per prompt
#             'size': '1024x1024'
#             # 'size' : '400x400'
#         }
        
#         response = requests.post('https://api.openai.com/v1/images/generations', headers=headers, json=payload)
        
#         print("Response Status Code: ", response.status_code)
#         print("Response Text: ", response.text)


#         if response.status_code == 200:
#             image_data = response.json()  # The JSON response contains the generated image.
#             image_url = image_data['data'][0]  # Assuming one image is generated per prompt
#             image_urls_list.append((description, image_url))
#             print(f"Image {i + 1}: {description}")
#             print(f"URL: {image_url}")
#         else:
#             print(f"Failed to generate image for description: {description}")

#     return image_urls_list


