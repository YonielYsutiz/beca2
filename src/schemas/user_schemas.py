from pydantic import BaseModel, EmailStr, Field
from typing import Optional

#Modelo para validacion de entrada de registro de usuarios
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8)
    fullname: Optional[str] = None
    number_phone : str = Field(min_length=10)
    date : str = Field(min_length= 3)

    class Config: 
        from_attributes = True  #Permite convertir objectos ORM a pydantic

class UserResponse(BaseModel):
    id: int
    username: str
    email : EmailStr
    fullname : Optional[str]
    number_phone: str
    date: Optional[str]

    class Config: 
        from_attributes = True  #Permite convertir objectos ORM a pydantic

class DeleteResponse(BaseModel):
    message: str
    deleted_user_id: int 
    
    class Config:
        from_attributes = True  #Permite convertir objectos ORM a pydantic

class LoginResponse(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    
    class Config:
        from_attributes = True
