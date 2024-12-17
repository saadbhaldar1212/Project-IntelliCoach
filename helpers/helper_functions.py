import json

from settings.config import config
from settings.logger_setup import logger

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader


x_api_key_header = APIKeyHeader(name="X-API-KEY")

def get_fitness_related_output(query: str, topics: list):
    try:
        response = config.CLIENT.chat.completions.create(
            model=config.OPENAI_API_MODEL,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "You are an Fitness Coach Expert who only answer for question which are related to Fitness, Gym and Health."
                },
                {
                    "role": "user",
                    "content": f"""{config.FITNESS_PROMPT.format(query=query, topics=topics)}"""
                },
            ],
            max_tokens=1000,
            temperature=0.0,
        )
        content = json.loads(response.choices[0].message.content)["answer"]
        return content
    except Exception as e:
        logger.exception(f"Error in helper_function: get_fitness_related_output: {str(e)}")
        raise e
    
def authenticate(x_api_key: str = Depends(x_api_key_header)):
    if x_api_key != config.x_api_authentication_key:
        logger.error(f"Invalid X-API-KEY given during authentication")
        raise HTTPException(status_code=401, detail="Invalid X-API-KEY")