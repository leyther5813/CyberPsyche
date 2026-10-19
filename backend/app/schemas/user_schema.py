from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class UserRegisterDTO(BaseModel):
    email: str
    password: str = Field(..., min_length=8)

class UserLoginDTO(BaseModel):
    email: str
    password: str

class UserResponseDTO(BaseModel):
    id: str
    email_hash: str
    role: str

class ConsentDTO(BaseModel):
    version: str = "1.0"
    accepted: bool = True

class DigitalContextDTO(BaseModel):
    life_stage: Optional[str] = None
    activities: List[str] = []
    cyber_level: Optional[str] = None
    interests: List[str] = []
