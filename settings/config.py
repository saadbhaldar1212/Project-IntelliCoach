"""Configuration module for fitness advisor chatbot.

Loads and manages all configuration settings including API keys, database
connections, and model configurations from environment variables.
"""

import os

from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError
from azure.search.documents import SearchClient

from google import genai

# from pymongo.mongo_client import MongoClient

from dotenv import find_dotenv, load_dotenv

from settings.logger_setup import logger


_ = load_dotenv(find_dotenv())


class Config:
    """
    Configuration class to load and manage application settings.
    """

    def __init__(self):
        try:
            # API Authentication Key
            self.x_api_authentication_key = os.environ["X_API_KEY"]

            # LLM Configurations
            self.llm_name = os.environ.get("LLM_NAME", "gemini-2.5-flash")
            self.llm_temperature = float(os.environ.get("LLM_TEMPERATURE", 0.1))
            self.llm_top_p = float(os.environ.get("LLM_TOP_P", 1.0))
            self.llm_max_output_tokens = int(
                os.environ.get("LLM_MAX_OUTPUT_TOKENS", 1024)
            )

            # Prompt
            self.fitness_prompt = """Given the query, you must only answer for question which are \
                related to the given topics. 
            Note: Any other question asked must be answered as "Question is out of context".
            query: {query}
            topics: {topics}
            Strictly provide the output in JSON format
            {{
                "answer": ""
            }}
            """
            self.is_greetings = """You are an AI Assistant who check if the question is \
                chit-chat/greetings or not.
            Question: {question}
            Strictly provide the output in JSON format
            {{
                "is_greetings_based": bool
            }}
            """
            self.greet_back = """You are an AI Assistant who greets back the user.
            Strictly provide the output in JSON format
            {{
                "greet_back": str
            }}
            """
            logger.info("Prompt Template initialized")

            # Gemini config
            self.gemini_api_key = os.environ["GEMINI_API_KEY"]
            logger.info("Gemini configurations initialized")

            # Gemini AI Embedding config
            self.gemini_client = genai.Client(api_key=self.gemini_api_key)
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

            self.local_faq_sheet_path = os.environ.get(
                "LOCAL_FAQ_SHEET_PATH", r".\database\Fitnessbot_allInOneQA.xlsx"
            )
            self.df_excel = None
            logger.info("FAQ Sheet path configuration initialized")

            self.azure_search_endpoint = os.environ.get("AZURE_SEARCH_ENDPOINT")
            self.azure_search_key = os.environ.get("AZURE_SEARCH_KEY")
            self.azure_search_index = os.environ.get(
                "AZURE_SEARCH_INDEX", "intellicoach-index"
            )

            if self.azure_search_endpoint and self.azure_search_key:
                try:
                    credential = AzureKeyCredential(self.azure_search_key)
                    self.search_client = SearchClient(
                        endpoint=self.azure_search_endpoint,
                        index_name=self.azure_search_index,
                        credential=credential,
                    )
                    logger.info("Azure Search client initialized")
                except AzureError as e:
                    logger.exception("Failed to initialize Azure Search client: %s", e)
                    self.search_client = None
            else:
                self.search_client = None

            # S3 / blob configuration (used by RAG pipeline)
            self.endpoint_url = os.getenv("ENDPOINT_URL")
            self.access_key = os.getenv("ACCESS_KEY")
            self.secret_key = os.getenv("SECRET_KEY")
            self.bucket_name = os.getenv("BUCKET_NAME")

            # File keys and local paths
            self.faq_sheet_key = os.getenv(
                "FAQ_SHEET_KEY", "faq_sheet/Fitnessbot_allInOneQA.xlsx"
            )
            self.secret_auth_key = os.getenv(
                "SECRET_AUTH_KEY", "intellicoach-fitness-chatbot-589e0fc60f1e.json"
            )
            self.local_secret_key_base = os.getenv(
                "LOCAL_SECRET_KEY_BASE",
                r"settings\intellicoach-fitness-chatbot-589e0fc60f1e.json",
            )
        except Exception as e:
            logger.exception("Error initializing Config: %s", str(e))
            raise RuntimeError(f"Error initializing Config: {str(e)}") from e


config = Config()
