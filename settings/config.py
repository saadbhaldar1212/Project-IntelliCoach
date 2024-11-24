import os

from openai import OpenAI
from dotenv import find_dotenv, load_dotenv
from pymongo.mongo_client import MongoClient

from settings.logger_setup import logger

_ = load_dotenv(find_dotenv())

class Config:
    def __init__(self):
        try:
            # API Authentication Key
            self.x_api_authentication_key = os.environ['X_API_KEY']

            # Prompt
            self.FITNESS_PROMPT = """Given the query, you must only answer for question which are related to Fitness, Gym and Health. 
            Note: Any other question asked must be answered as "Question is out of context".
            
            query: {query}
            Strictly provide the output in JSON format
            {{
                "answer": ""
            }}
            """
            logger.info('Promp Template initialized')

            # OpenAI config
            self.OPENAI_API_KEY = os.environ['OPENAI_API_KEY'] 
            self.OPENAI_API_MODEL = os.environ['OPENAI_API_MODEL']
            self.CLIENT = OpenAI(api_key=self.OPENAI_API_KEY)
            logger.info('OpenAI configurations initialized')

            # MongoDB config
            self.client = MongoClient(os.environ['MONGODB_URI'])
            self.db = self.client["db-fitness-chatbot"]
            self.user_collection = self.db["users"]
            logger.info('Database configurations initialized')
        except Exception as e:
            logger.exception(f"Error in helper_function: get_fitness_related_output: {str(e)}")
            raise Exception(f"Error in helper_function: get_fitness_related_output: {str(e)}")
        
config = Config()