from fastapi import FastAPI
import httpx
import asyncio
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

BUSINESS_SERVICE_URL = os.getenv("BUSINESS_SERVICE_URL", "http://business_service:8000")

@app.on_event("startup")
async def startup_event():
    logger.info(f"Scheduler service started. Calling {BUSINESS_SERVICE_URL}/status every 10 seconds.")
    asyncio.create_task(call_business_service_periodically())

async def call_business_service_periodically():
    async with httpx.AsyncClient() as client:
        while True:
            try:
                logger.info(f"Attempting to call {BUSINESS_SERVICE_URL}/status")
                response = await client.get(f"{BUSINESS_SERVICE_URL}/status")
                response.raise_for_status()

                response_data = response.json() 
                logger.info(f"Successfully called business service: {response_data}")

            except httpx.RequestError as e:
                logger.error(f"Error calling business service: {e}")
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error calling business service: {e.response.status_code} - {e.response.text}")
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
            await asyncio.sleep(10)

@app.get("/status")
async def get_status():
    return {"status": "Scheduler service is running and calling business_service."}