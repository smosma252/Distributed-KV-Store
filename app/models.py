from pydantic import BaseModel

class KVRequest(BaseModel):
    key:str
    value:str
