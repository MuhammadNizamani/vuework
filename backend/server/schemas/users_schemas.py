import strawberry
from typing import Annotated, Union


# Define GraphQL types
@strawberry.type
class UserType:
    user_id: int
    name: str
    email: str
    chess_username: str
    
   
# @strawberry.type
# class SignupError:
#     message: str 
@strawberry.type
class SignUpResult:
    success: bool
    user: Union[UserType, None]
    message: str


@strawberry.input
class UserInput:
    name: str
    email: str
    password: str
    chess_username: str
    def to_dict(self):
        return {
            "name": self.name,
            "chess_username": self.chess_username,
            "email": self.email,
            "password": self.password,
        }

@strawberry.type
class LoginSuccess:
    user: UserType


@strawberry.type
class LoginError:
    message: str


# LoginResult = Annotated[
#     Union[LoginSuccess, LoginError], strawberry.union("LoginResult")
# ]

# SignUpResult = Annotated[
#     Union[UserType, SignupError], strawberry.union("SignUpResult")
# ]