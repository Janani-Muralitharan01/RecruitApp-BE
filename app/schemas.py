import array
from fastapi import FastAPI, Form
from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr, constr
from bson.objectid import ObjectId


class UserBaseSchema(BaseModel):
    name: str
    email: str
    photo: str | None = None
    role: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    Designation: str | None = None
    Gender: str | None = None
    DateofBirth: str | None = None
    PhoneNumber: str | None = None

    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8)
    passwordConfirm: str
    verified: bool = False


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class CreatelogoSchema(BaseModel):
    tittle: str
    profile: str


class UserResponseSchema(UserBaseSchema):
    id: str
    pass


class createNewUserSchema(UserBaseSchema):
    id: str
    pass


class UserResponse(BaseModel):
    status: str
    user: UserResponseSchema


class AllUserResponse(BaseModel):
    status: str
    user: createNewUserSchema


class FilteredUserResponse(UserBaseSchema):
    id: str


class FormBaseSchema(BaseModel):
    title: str
    content: str
    category: str
    image: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class CreateFormSchema(FormBaseSchema):
    user: ObjectId | None = None
    pass


class FormResponse(FormBaseSchema):
    id: str
    user: FilteredUserResponse
    created_at: datetime
    updated_at: datetime


class UpdateFormSchema(BaseModel):
    title: str | None = None
    content: str | None = None
    category: str | None = None
    image: str | None = None
    user: str | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ListFormResponse(BaseModel):
    status: str
    results: int
    posts: List[FormResponse]


class createNewUserSchema(UserBaseSchema):
    Designation: str
    Gender: str
    DateofBirth: str
    PhoneNumber: str


class updateUserSchema(BaseModel):
    name: str
    Designation: str
    Gender: str
    DateofBirth: str
    PhoneNumber: str
    photo: str


class formsSchema(BaseModel):
    modulename: str | None = None
    recuriter: str
    created_at: datetime | None = None
    moduleelements: dict | None = None
    tableData: dict | None = None


class tabledataSchema(BaseModel):
    moduleId: str
    recuriter: str
    created_at: datetime | None = None
    tableData: dict | None = None


class updateformSchema(BaseModel):
    modulename: str
    created_at = datetime.utcnow()
    moduleelements: dict | None = None
    tableData: dict | None = None


class formvalueSchema(BaseModel):
    moduleelements: dict | None = None


class userlogoSchema(BaseModel):
    created_at: datetime | None = None
