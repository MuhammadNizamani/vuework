import strawberry
from typing import Annotated, Union


# Define GraphQL types
@strawberry.type
class UserType:
    user_id: int
    name: str
    email: str

@strawberry.input
class UserInput:
    name: str
    email: str
    password: str

@strawberry.type
class LoginSuccess:
    user: UserType


@strawberry.type
class LoginError:
    message: str


LoginResult = Annotated[
    Union[LoginSuccess, LoginError], strawberry.union("LoginResult")
]