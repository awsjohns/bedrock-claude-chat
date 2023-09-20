from typing import Literal

from humps import camelize
from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    class Config:
        alias_generator = camelize
        populate_by_name = True


class Content(BaseSchema):
    content_type: Literal["text"] = Field(..., description="Currently")
    body: str


class MessageInput(BaseSchema):
    role: str
    content: Content
    model: Literal["titan", "claude"]


class MessageOutput(BaseSchema):
    id: str
    role: str
    content: Content
    model: Literal["titan", "claude"]


class ChatInput(BaseSchema):
    conversation_id: str = Field("", description="Conversation ID")
    message: MessageInput = Field(..., description="inside the message")


class ChatInputWithToken(ChatInput):
    token: str


class ChatOutput(BaseSchema):
    conversation_id: str | None = Field(...)
    message: MessageOutput = Field(..., description="of the message")
    create_time: float = Field(..., description="Created date")


class ConversationMeta(BaseSchema):
    id: str
    title: str
    create_time: float


class Conversation(BaseSchema):
    id: str
    title: str
    create_time: float
    messages: list[MessageOutput] = Field(..., description="inside the message")


class NewTitleInput(BaseSchema):
    new_title: str


class ProposedTitle(BaseSchema):
    title: str


class User(BaseSchema):
    id: str
    name: str
