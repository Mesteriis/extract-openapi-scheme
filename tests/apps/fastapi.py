# flake8: noqa
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(description="Test app", version="0.1.0")


class Item(BaseModel):
    id: int
    name: str


@app.post("/items/", tags=["Items"])
async def create_item(item: Item) -> Item:
    return item


@app.get("/items/", tags=["Items"])
async def read_items() -> list[Item]:
    return [
        Item(id=1, name="Portal Gun"),
        Item(id=2, name="Plumbus"),
    ]
