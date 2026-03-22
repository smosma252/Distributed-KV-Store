from fastapi import FastAPI
from fastapi import HTTPException
from app.models import KVRequest
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
app = FastAPI()

kv_memory_store = {}

@app.get('/')
def root():
    return kv_memory_store

@app.post('/kv')
async def add_key(req:KVRequest):
    key = req.key
    value = req.value
    if key in kv_memory_store:
        logger.info("Key is already present.")
        return {"message": f"{key} is already present."}
    logger.info("Key has been added.")
    kv_memory_store[key] = value

@app.get('/kv/{key}')
async def get_key(key):
    if key not in kv_memory_store:
        logger.info("Key is not present.")
        return {"message": f"{key} is not present."}
    logger.info("Returned value from store.")
    return {f"{key}": f"{kv_memory_store[key]}"}

@app.delete('/kv')
async def remove_user(key:str):
    if key not in kv_memory_store:
        logger.info("Key is not present.")
        return {"message": f"{key} is not present or already deleted"}
    del kv_memory_store[key]
    logger.info("Key has been deleted.")
    return {"message": f"{key} has been deleted"}
