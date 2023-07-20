from pydantic import BaseModel


class UserSchemas(BaseModel):
    username: str
    fullname: str
    password: str
