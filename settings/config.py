import os
import pandas as pd

from openai import OpenAI

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from pymongo.mongo_client import MongoClient

from settings.logger_setup import logger

from dotenv import find_dotenv, load_dotenv

_ = load_dotenv(find_dotenv())


class Config:
    def __init__(self):
        try:
            # API Authentication Key
            self.x_api_authentication_key = os.environ["X_API_KEY"]

            # Prompt
            self.FITNESS_PROMPT = """Given the query, you must only answer for question which are related to the given topics. 
            Note: Any other question asked must be answered as "Question is out of context".
            query: {query}
            topics: {topics}
            Strictly provide the output in JSON format
            {{
                "answer": ""
            }}
            """
            self.IS_GREETINGS = """You are an AI Assistant who check if the question is chit-chat/greetings or not.
            Question: {question}
            Provide the answer in following JSON format.
            {{
                "is_greetings_based": bool
            }}
            """
            self.GREET_BACK = """You are an AI Assistant who greets back the user.
            Provide the answer in following JSON format.
            {{
                "greet_back": str
            }}
            """
            logger.info("Prompt Template initialized")

            # OpenAI config
            self.OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
            self.OPENAI_API_MODEL = os.environ["OPENAI_API_MODEL"]
            self.CLIENT = OpenAI(api_key=self.OPENAI_API_KEY)
            logger.info("OpenAI configurations initialized")

            # OpenAI Embedding config
            self.OPENAI_EMBEDDING_MODEL = os.environ["OPENAI_EMBEDDING_MODEL"]
            self.OPENAI_EMBEDDING_API_KEY = os.environ["OPENAI_EMBEDDING_API_KEY"]
            logger.info("OpenAI Embedding configurations initialized")

            # MongoDB config
            self.client = MongoClient(os.environ["MONGODB_URI"])
            self.db = self.client["db-fitness-chatbot"]
            self.user_collection = self.db["users"]
            logger.info("Database configurations initialized")

            # FAQ Sheet
            self.df_excel = pd.read_excel(
                r"D:\GitHub\Fitness_Advisor\3.10\fitness_advisor_chatbot\fitness_advisor_chatbot_v3.10\database\chroma\Fitnessbot_allInOneQA.xlsx"
            )
            logger.info("FAQ Sheet initialized")

            # FAQ VDB
            self.EMBEDDING_CLIENT = OpenAIEmbeddings(model=self.OPENAI_EMBEDDING_MODEL)
            self.vdb = Chroma(
                embedding_function=self.EMBEDDING_CLIENT,
                persist_directory=r"D:\GitHub\Fitness_Advisor\3.10\fitness_advisor_chatbot\fitness_advisor_chatbot_v3.10\database\chroma\FitnessBot_Questions_VDB",
            )
        except Exception as e:
            logger.exception(
                f"Error in helper_function: get_fitness_related_output: {str(e)}"
            )
            raise Exception(
                f"Error in helper_function: get_fitness_related_output: {str(e)}"
            )


config = Config()
