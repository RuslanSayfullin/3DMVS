from pydantic import BaseModel

class Todo(BaseModel):
    id: int
    item: str

class TodoItem(BaseModel):
    item: str
    
    class Config:
        schema_extras = {
            "example": {
                "item": "Read the next chapter od the book"
            }
        }