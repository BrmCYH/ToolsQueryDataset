from typing import List, Optional, Dict, Union, Callable, Literal
from enum import Enum, unique
from pydantic import BaseModel, Field
import openai

@unique
class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    FUNCTION = "function"
    TOOL = "tool"
class ChatMessage(BaseModel):
    role: Optional[Role]
    content: str