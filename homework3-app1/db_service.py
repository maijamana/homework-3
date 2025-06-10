from fastapi import FastAPI, Request

app = FastAPI()
storage_unit = []

@app.get("/")
async def get_info():
    return {"service_description": "Data persistence layer for microservice ecosystem."}

@app.get("/status")
async def check_status():
    return {"operational_status": "active"}

@app.post("/store_record") # ЦЕ НОВИЙ ЕНДПОІНТ: /store_record
async def store_record_entry(incoming_request: Request):
    new_record = await incoming_request.json()
    storage_unit.append(new_record)
    return {"status_message": "record stored", "entry": new_record}

@app.get("/retrieve_latest") # ЦЕ НОВИЙ ЕНДПОІНТ: /retrieve_latest
async def retrieve_last_entry():
    if storage_unit:
        return {"latest_data": storage_unit[-1]}
    return {"latest_data": None}