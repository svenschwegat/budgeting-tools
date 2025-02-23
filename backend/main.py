# start with fastapi dev main.py

import uvicorn
from typing import List
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File

import parse_bank_statement_pdf


class Item(BaseModel):
    name: str

class Items(BaseModel):
    items: List[Item]

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_db = {"items": []}

@app.get("/items", response_model=Items)
def get_items():
    return Items(items=memory_db["items"])

@app.post("/items")
def add_item(item: Item, response_model=Item):
    memory_db['items'].append(item)
    return item

@app.post("/parse-pdf")
async def parse_pdf(): #file: UploadFile = File(...)
    #contents = await file.read()
    #with open("temp.pdf", "wb") as f:
    #    f.write(contents)

    result = parse_bank_statement_pdf #.parse("temp.pdf")
    
    return {"result": result}

if(__name__ == "__init__"):
    uvicorn.run(app, host="0.0.0.0", port=8000)