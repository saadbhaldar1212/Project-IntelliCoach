import uvicorn

from fastapi import FastAPI, Depends
from dotenv import find_dotenv, load_dotenv

from settings.logger_setup import logger
from settings.config import config

from helpers.helper_functions import get_fitness_related_output, authenticate
from model.query import QueryRequest, QueryResponse

from database.user_schema import list_users

_ = load_dotenv(find_dotenv())
logger.info('Environment Keys initialized')

app = FastAPI()
logger.info('FastAPI initialized')

@app.post('/query')
async def fitness_query(
    query: QueryRequest, _: None = Depends(authenticate)
) -> QueryResponse:
    try:
        fitness_query_output = get_fitness_related_output(query=query)
        properties = {
            "custom_dimensions": {
                "incoming_query": query,
                "answer": fitness_query_output
            }
        }
        logger.info("fitness_query_output: %s", properties, extra=properties)
        return QueryResponse(
            success=True,
            answer=fitness_query_output
        )
    except Exception as e:
        properties = {
            "custom_dimensions": {
                "incoming_query": query,
                "error_message": str(e)
            }
        }
        logger.exception("Error in fitness_query: %s", properties, extra=properties)
        return QueryResponse(
            success=False,
            error_message=str(e)
        )
@app.post("/user")
async def get_all_users():
    """
    The function `get_all_bags` retrieves all bags from a bag collection asynchronously in Python.
    """
    users = list_users(config.user_collection.find())
    return users
    
if __name__ == "__main__":
    logger.info('Starting Uvicorn Server')
    try:
        uvicorn.run(app, host='0.0.0.0', port=8000) 
    except Exception as e:
        logger.error("Error starting in Uvicorn server")
        raise e
    logger.error('Uvicorn Server stopped.')
