from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

@app.get("/")
async def get_root_description():
    return {"service_info": "Text processing unit for analytical tasks."}

@app.get("/status")
async def get_service_status():
    return {"status_check": "operational"}

@app.post("/analyze")
async def analyze_input_text(input_data: dict):
    input_text = input_data.get("input_string", "")
    if not isinstance(input_text, str):
        return {"issue": "Invalid data format: 'input_string' must be text"}, 400

    await asyncio.sleep(2)

    text_words = input_text.split()
    total_words = len(text_words)
    contains_query = "?" in input_text
    capitalized_tokens = [token for token in text_words if token.isupper()]

    result = {
        "source_text": input_text,
        "token_count": total_words,
        "is_question_present": contains_query,
        "all_caps_tokens": capitalized_tokens,
        "analysis_time": time.time()
    }

    return result