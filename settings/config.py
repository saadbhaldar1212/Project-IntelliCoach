import os
import pandas as pd

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# from pymongo.mongo_client import MongoClient

from dotenv import find_dotenv, load_dotenv

from settings.logger_setup import logger


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
            Strictly provide the output in JSON format
            {{
                "is_greetings_based": bool
            }}
            """
            self.GREET_BACK = """You are an AI Assistant who greets back the user.
            Strictly provide the output in JSON format
            {{
                "greet_back": str
            }}
            """
            logger.info("Prompt Template initialized")

            # LLAMA config
            self.HF_TOKEN = os.environ["HF_TOKEN"]
            self.API_URL = os.environ["API_URL"]
            self.LLAMA_MODEL = os.environ["LLAMA_MODEL"]
            logger.info("OpenAI configurations initialized")

            # Gemini AI Embedding config
            self.GEMINI_EMBEDDING_MODEL = os.environ["GEMINI_EMBEDDING_MODEL"]
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
                r".\settings\intellicoach-fitness-chatbot-589e0fc60f1e.json"
            )
            print("Google Application Credentials set")
            logger.info("Gemini AI Embedding configurations initialized")

            # MongoDB config
            # self.client = MongoClient(os.environ["MONGODB_URI"])
            # self.db = self.client["db-fitness-chatbot"]
            # self.user_collection = self.db["users"]
            # logger.info("Database configurations initialized")

            # FAQ Sheet
            self.df_excel = pd.read_excel(
                r".\database\chroma\Fitnessbot_allInOneQA.xlsx"
            )
            logger.info("FAQ Sheet initialized")

            # FAQ VDB
            self.EMBEDDING_CLIENT = GoogleGenerativeAIEmbeddings(
                model=self.GEMINI_EMBEDDING_MODEL,
                # credentials=
            )
            self.vdb = Chroma(
                embedding_function=self.EMBEDDING_CLIENT,
                persist_directory=r".\database\chroma\FitnessBot_Questions_VDB",
            )
        except Exception as e:
            logger.exception(
                f"Error in helper_function: get_fitness_related_output: {str(e)}"
            )
            raise Exception(
                f"Error in helper_function: get_fitness_related_output: {str(e)}"
            )


config = Config()
