

from dotenv import load_dotenv
from flask import jsonify
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.schema import BaseOutputParser
import os

class CommaOutputParser(BaseOutputParser):

    def parse(self,text):
        item = text.strip().split(",")
        return list(map(str.strip,item))

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")


chat = ChatOpenAI(
    temperature=0.1,
)


def script(user_script):
    try:
        # Prepare the chat prompt template
        template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You will now become an expert on the following topic: [{user_script}]. You must write a video script of 200 words for a YouTube short in korean. you must write script in KOREAN: The output should only contain the content of the script. Any arbitrary intros, outros, or explanatory statements outside the main content are to be excluded from the output. The script must follow these criteria: There is an initial statement, and the subsequent statements support the initial statement with scientific facts or historical evidence. The body of the video includes additional explanations about the topic under discussion. Additional explanations include scientific facts and historical evidence that augment the initial statement. The script must only contain the narrative content without any additional script features like camera directions or scene transitions. Each sentence must be specific, concise, and use professional language. The content should be engaging and addictive to suit the nature of YouTube shorts. When outputting, only the narrative content of the script should be presented in a continuous prose format without any stage directions or background music descriptions."
        ),
        ("human", f"Please write a script about {user_script}. The script you will write is for producing a YouTube short. Make sure it is engaging enough to hook the viewers and keep them focused to prevent drop-offs during the video. Also, ensure the video does not exceed one minute.")
    ]
)

        # Execute the chain of operations: template formatting, chat model prediction, and parsing
        chain = template | chat | CommaOutputParser()
        theme_list = chain.invoke({"user_script": user_script})

        # theme_list should be a list of strings if everything goes well
        print(theme_list)

        # Make sure to return a serializable Python object (e.g., list or dict)
        if isinstance(theme_list, list):
            return theme_list  # Return the list directly if it's a list
        else:
            raise ValueError("The returned value is not a list.")  # Raise an error if it's not a list

    except Exception as e:
        # Here you should NOT use jsonify since this function should return a Python object, not a Flask response
        # This exception will be handled by Flask's error handling in the route
        print(f"Error: {e}")
        raise e