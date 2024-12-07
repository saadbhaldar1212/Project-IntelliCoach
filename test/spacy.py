# https://spacy.io/models

# py -m pip install spacy uvicorn fastapi
# python -m spacy download en_core_web_sm

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import spacy, uvicorn

# Initialize FastAPI
app = FastAPI()

# Load the spaCy model (you can choose an appropriate model like en_core_web_sm)
nlp = spacy.load("en_core_web_sm")

# Example of a simple text classifier (dynamic intent classification)
def classify_intent(message: str) -> str:
    """
    This is a simple example of dynamic intent classification.
    In practice, you would train a model for intent classification.
    """
    # Convert message to lowercase and process using spaCy's NLP pipeline
    doc = nlp(message.lower())
    print(doc)

    # Example classification rules based on specific keywords or patterns (You can extend this)
    if any(token.text in ["hello", "hi", "hey", "greetings", "good morning", "good evening"] for token in doc):
        return "greeting"
    else:
        return "other"

@app.post("/webhook/")
async def spacy_webhook(request: dict):
    """
    Endpoint to send messages to spaCy and get a response.
    """
    user_message = request.get("message")
    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required.")
    
    # Handle the incoming message and get the response
    response = await handle_message(user_message)
    return JSONResponse(content=response)

async def handle_message(message: str):
    """
    Process the message, detect intent, and return the appropriate response.
    """
    try:
        # Dynamically classify the intent of the message
        intent = classify_intent(message)

        # Handle the response based on the intent
        if intent == "greeting":
            response = {"responses": [{"text": "Hello! How can I assist you today?"}], "intent": intent}
        else:
            response = {"responses": [{"text": message}], "intent": intent}

        return response
    
    except Exception as e:
        raise RuntimeError(f"Error while processing message: {e}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the dynamic intent detection with spaCy!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)