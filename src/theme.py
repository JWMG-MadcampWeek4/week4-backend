from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.schema import BaseOutputParser
import os

class CommaOutputParser(BaseOutputParser):
    def parse(self, text):
        items = text.strip().split(",")
        return list(map(str.strip, items))

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")

chat = ChatOpenAI(
    temperature=0.1,
)

def theme(user_theme):
    try:
        template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a YouTube shorts theme recommendation machine. For the specific theme '{user_theme}' provided by the user, recommend the names of five related specific events or topics. For instance, if '{user_theme}' is 'historically significant events,' then list actual events such as 'world war ii, french revolution, cultural revolution, cold war, trojan war' in list format. The list should consist only of event names in lowercase, separated by commas. Provide the list directly without any additional explanations, intros, or outros, and conclude the response after the list is complete. If the provided theme is invalid, respond with 'fail'. Use only Korean and the specified list format."
        ),
        ("human", f"I want to create YouTube shorts based on the theme '{user_theme}'. Please recommend a comma-separated list of names of related specific events or topics.")
    ]
)

        chain = template | chat | CommaOutputParser()
        theme_list = chain.invoke({"user_theme": user_theme})

        if isinstance(theme_list, list):
            return theme_list
        else:
            raise ValueError("The returned value is not a list.")

    except Exception as e:
        print(f"Error: {e}")
        raise e