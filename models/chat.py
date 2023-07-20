from pydantic import BaseModel

class ChatItem(BaseModel):
    question: str