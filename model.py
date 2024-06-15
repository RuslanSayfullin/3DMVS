from pydantic import BaseModel
from typing import List, Optional

class Todo(BaseModel):
    id: int
    item: str

class TodoItem(BaseModel):
    item: str
    
    @classmethod
    def as_form(
        cls,
        item: str = Form(...)
    ):
        return cls(item=item)

class TodoItems(BaseModel):
    todos: List[TodoItem]

    class Config:
        schema_extra = {
            "example": {
            "todos": [
                    {
                        "item": "Example schema 1!"
                    },
                    {
                        "item": "Example schema 2!"
                    }
                ]
            }
        }