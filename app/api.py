from fastapi import FastAPI
from fastapi import HTTPException
from threading import Lock
from app.models import KVRequest
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
app = FastAPI()

key_lock= Lock()
kv_memory_store = {} 

@app.get('/')
def root():
    return kv_memory_store

@app.post('/kv')
async def add_key(req:KVRequest):
    key = req.key
    value = req.value
    with key_lock:
        if key in kv_memory_store:
            logger.info("Key is already present.")
            raise HTTPException(status_code=409, detail="key is already present")
        logger.info("Key has been added.")
    kv_memory_store[key] = value

@app.get('/kv/{key}')
async def get_key(key):
    if key not in kv_memory_store:
        logger.info("Key is not present.")
        return HTTPException(status_code=422, detail="key is not present")
    logger.info("Returned value from store.")
    return {f"{key}": f"{kv_memory_store[key]}"}

@app.delete('/kv')
async def remove_user(key:str):
    with key_lock:
        if key not in kv_memory_store:
            logger.info("Key is not present.")
            return HTTPException(status_code=422, detail="key has already been deleted or not found.")
        del kv_memory_store[key]
    logger.info("Key has been deleted.")
    return {"message": f"{key} has been deleted"}
