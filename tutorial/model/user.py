from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
    '''
    Base model for User
    '''
    username: str = Field(
        ...,
        example='peeeeeter_j',
    )
    email: EmailStr = Field(
        ...,
        example='peter.j@kakao.com',
    )
    full_name: Optional[str] = Field(
        None,
        example='Peter Johannes Jung',
    )

class UserIn(UserBase):
    '''
    Class for the creation of the user
    '''
    password: str = Field(
        ...,
        example='ku201711424',
    )

class UserOut(BaseModel):
    '''
    Class for return from the creation of the user
    '''
    pass

class UserInDB(BaseModel):
    '''
    Class for store the user in database
    '''
    hashed_password: str = Field(
        ...,
    )
