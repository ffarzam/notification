from pydantic import BaseModel, EmailStr


class BaseNotification(BaseModel):
    email: EmailStr
    action: str

