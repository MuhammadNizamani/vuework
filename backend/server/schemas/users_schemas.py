import strawberry
from typing import Annotated, Union
from datetime import datetime

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

# @strawberry.type
# class LoginSuccess:
#     user: UserType


# @strawberry.type
# class LoginError:
#     message: str


# LoginResult = Annotated[
#     Union[LoginSuccess, LoginError], strawberry.union("LoginResult")
# ]

# SignUpResult = Annotated[
#     Union[UserType, SignupError], strawberry.union("SignUpResult")
# ]

@strawberry.type
class LoginType:
    user_id: int
    name: str
    email: str
    chess_username: str
    avater: str
    last_online : datetime
    league : str
    country: str
    followers: int
    player_id:str
    status : str
    is_streamer: bool
    verified:bool   


@strawberry.type
class LoginResult:
    success: bool
    login: Union[LoginType, None]
    message: str
    
@strawberry.type
class RatingType:
    user_id: int
    daily_rating: Union[int, None]
    rapid_rating: Union[int, None]
    blitz: Union[int, None]
    bullet_rating: Union[int, None]
    