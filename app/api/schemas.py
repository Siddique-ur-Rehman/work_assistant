
from pydantic import BaseModel, Field


class ChatIn(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


class RenameIn(BaseModel):
    title: str = Field(min_length=1, max_length=100)