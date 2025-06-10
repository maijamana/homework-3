from fastapi import FastAPI, Header, HTTPException, status
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
AUTH_SECRET_TOKEN = os.getenv("APP_TOKEN")

app = FastAPI()

DB_SERVICE_URL = os.getenv("DB_SERVICE_URL", "http://localhost:8002")
BUSINESS_SERVICE_URL = os.getenv("BUSINESS_SERVICE_URL", "http://localhost:8001")

@app.get("/")
async def get_root_info():
    return {"service_description": "This is the Client Orchestration Service. Use /execute_workflow to start processing."}

@app.get("/status")
async def check_service_status():
    return {"health_status": "online"}

@app.post("/execute_workflow")
async def execute_processing_workflow(authorization: str = Header(None)):
    if authorization != f"Bearer {AUTH_SECRET_TOKEN}":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please provide a valid Bearer token."
        )

    async with httpx.AsyncClient() as client:
        try:
            db_read_response = await client.get(f"{DB_SERVICE_URL}/retrieve_latest")
            db_read_response.raise_for_status()
            retrieved_payload = db_read_response.json().get("latest_data")

            if not retrieved_payload:
                print("No data found in DB service. Using default payload.")
                payload_for_business = {"input_string": "default text for processing"}
            else:
                payload_for_business = {"input_string": retrieved_payload.get("original_text", "default text")}


            business_process_response = await client.post(f"{BUSINESS_SERVICE_URL}/analyze", json=payload_for_business)
            business_process_response.raise_for_status()
            processed_output = business_process_response.json()

            db_write_response = await client.post(f"{DB_SERVICE_URL}/store_record", json=processed_output) # <<<<<< УВАГА: Тут має бути /store_record
            db_write_response.raise_for_status()

            return processed_output

        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Downstream service unavailable: {exc.request.url} - {exc}"
            )
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Error from downstream service {exc.request.url}: {exc.response.text}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {e}"
            )