import strawberry
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
