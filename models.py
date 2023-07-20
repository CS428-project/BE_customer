from pydantic import BaseModel

"""
class <classname>(BaseModel):
    <variable>: <type> = <value>
"""


#               STRUCTURE DEFINE
class SignUpSchema(BaseModel):
    email: str
    password: str


class AccountInfo(BaseModel):
    userID: str = "123456"
    username: str = "ltnhan"
    password: str = "Nhan123@"
    created_at: str = "01-01-2000"


class UserInfo(BaseModel):
    userID: str = "123456"
    fname: str = "Le"
    lname: str = "Nhan"
    email: str = "ltnhan@gmail.com"
    phone: str = "0123456789"
    dob: str = "01-01-2000"
    country: str = "Vietnam"
    gender: bool = 0  # 0 male, 1 female
    role: bool = 0  # 0 mentee, 1 mentor


class MentorInfo(BaseModel):
    mentorID: str = "123456"
    fieldID: str = "123456"
    language: str = "English"
    description: str = "Hello"
    rating: float = 1.5


class Field(BaseModel):
    fieldID: str = "123456"
    fieldName: str = "business"


class Experience(BaseModel):
    userID: str = "123456"
    position: str = "CEO"
    workplace: str = "Google"
    startdate: str = "01-01-2023"
    enddate: str = "01-01-2025"
