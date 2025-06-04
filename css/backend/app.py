from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import openai
import os

# Load your OpenAI API key from environment variable or config
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class AskRequest(BaseModel):
    text: str

@app.post("/ask")
async def ask(request: AskRequest):
    try:
        # Call OpenAI GPT-4 API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are XARVIS-AI, a helpful assistant."},
                {"role": "user", "content": request.text}
            ],
            max_tokens=512,
            temperature=0.7
        )
        answer = response.choices[0].message["content"].strip()
        return JSONResponse(content={"response": answer})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)