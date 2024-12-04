# pip install fastapi uvicorn rasa

# rasa init

# rasa train

import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from rasa.core.agent import Agent
from rasa.core.interpreter import RasaNLUInterpreter
from rasa.core.processor import MessageProcessor

# Initialize FastAPI
app = FastAPI()

# Define Rasa agent path
RASA_PRO_LICENSE = ""
RASA_MODEL_PATH = "models/20211210-163533-my-model.tar.gz"  # Replace with your model path

# Initialize Rasa agent (load the trained model)
def load_rasa_agent():
    try:
        agent = Agent.load(RASA_MODEL_PATH)
        return agent
    except Exception as e:
        raise RuntimeError(f"Error loading Rasa model: {e}")

# Create a global variable for the loaded agent
agent = load_rasa_agent()

@app.post("/webhook/")
async def rasa_webhook(request: dict):
    """
    Endpoint to send messages to Rasa and get a response.
    """
    user_message = request.get("message")
    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required.")
    
    # Handle the incoming message and get the Rasa response
    response = await handle_message(user_message)
    return JSONResponse(content=response)

async def handle_message(message: str):
    """
    Send user message to Rasa agent and get a response.
    """
    try:
        # Process the message and get a response from the agent
        responses = await agent.handle_text(message)
        
        # Check for the intent in the response
        if responses:
            intent = responses[0].get("intent", {}).get("name")
            
            if intent == "greet":  # Only process if the intent is "greet"
                # Return the Rasa response
                return {"responses": responses}
            else:
                # Return the message as is if intent is not "greet"
                return {"responses": [{"text": message}]}
        else:
            # If no response, just return the message
            return {"responses": [{"text": message}]}
    
    except Exception as e:
        raise RuntimeError(f"Error while processing message: {e}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Rasa FastAPI integration!"}
