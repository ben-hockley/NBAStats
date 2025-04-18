from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    email: str
    hashed_password: str
    is_active: bool = True
    is_admin: bool = False