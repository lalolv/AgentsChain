from pydantic import BaseModel
from typing import Union, NamedTuple


class ChatItem(BaseModel):
    question: str

# stream 输出
class StreamOutput(NamedTuple):
    action: str
    outputs: Union[str, None] = ''
