import uvicorn

from fastapi import FastAPI, Depends
from dotenv import find_dotenv, load_dotenv

from settings.logger_setup import logger

from helpers.helper_functions import authenticate, query_llm
from model.query import QueryRequest, QueryResponse

_ = load_dotenv(find_dotenv())
logger.info("Environment Keys initialized")

app = FastAPI()
logger.info("FastAPI initialized")


@app.get("/")
async def root():
    """
    :return: A dictionary with a key "message" and a value "Welcome to Fitness Chatbot" is being
    returned.
    """
    return {"message": """Welcome to Fitness Chatbot"""}


@app.post("/query")
async def fitness_query(
    query: QueryRequest, _: None = Depends(authenticate)
) -> QueryResponse:
    """
    Function processes a query by calling `fitness_query` workflow and returns a response.
    """
    try:
        source, response = query_llm(query=query.incoming_query, topics=query.topics)
        return QueryResponse(
            success=True, answer=response, topics=query.topics, source=source
        )
    except Exception as e:
        properties = {
            "custom_dimensions": {
                "incoming_query": query,
                "error_message": str(e),
                "topics": query.topics,
                "source": source,
            }
        }
        logger.exception("Error in fitness_query: %s", properties, extra=properties)
        return QueryResponse(
            success=False,
            error_message=str(e),
        )


# @app.post("/user")
# async def get_all_users():
#     """
#     The function `get_all_bags` retrieves all bags from a bag collection asynchronously in Python.
#     """
#     users = list_users(config.user_collection.find())
#     return users


if __name__ == "__main__":
    logger.info("Starting Uvicorn Server")
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            server_header=False,
        )
    except Exception as e:
        logger.error("Error starting in Uvicorn server")
        raise e
    logger.error("Uvicorn Server stopped.")
