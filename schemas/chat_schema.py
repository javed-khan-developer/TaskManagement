from pydantic import BaseModel


class ChatRequest(BaseModel):

    title: str


class ChatCreate(ChatRequest):
    pass


class MessageRequest(BaseModel):

    message: str


class ChatResponse(BaseModel):

    id: int

    title: str

    class Config:
        from_attributes = True