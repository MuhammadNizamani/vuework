import strawberry
from server.models.models import Users, session
from fastapi.routing import APIRouter, Response
from fastapi import HTTPException, status
from server.schemas.users_schemas import UserInput, UserType, LoginResult , LoginSuccess, LoginError
import typing
from server.utils import helper
# import strawberry.asgi 
from strawberry.asgi import GraphQL

router = APIRouter(prefix="/users", tags=["User Router"])

@router.get("/data/{user_id}")
def get_user(user_id: int):
    user = session.query(Users).filter(Users.user_id == user_id).first()
    return user

@strawberry.type
class Query:
    @strawberry.field
    def user(self, user_id: int) -> UserType or str:
        query = session.query(Users).filter(Users.user_id == user_id).first()
        return query

    @strawberry.field
    def users(self) -> typing.List[UserType]:
        return session.query(Users).all()
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, info, name: str, email: str, password: str) -> str:
        hashed_password = helper.hash(password)
        new_user = Users(name=name, email=email, password=hashed_password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return "name: " + name+ " email: "+email

    @strawberry.mutation
    def update_user(self, info, id: int, name: str, email: str, password: str) ->  str:
        user_query = session.query(Users).filter(Users.user_id == id)
        user = user_query.first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id: {id} does not exist",
            )

        user.name = name
        user.email = email
        user.password = password
        session.commit()
        return user

    @strawberry.mutation
    def delete_user(self, info, id: int) -> str:
        user_query = session.query(Users).filter(Users.user_id == id)
        user = user_query.first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id: {id} does not exist",
            )

        user_query.delete(synchronize_session=False)
        session.commit()
        return "User deleted successfully"
    @strawberry.mutation
    def login_user(self ,email:str, password: str) -> str: # LoginResult:
        print("I am in login user function")
        user = session.query(Users).filter(Users.email == email).first()
        if user is None:
            return "Invalid Credentials"
        print(str(user.password))
        if not helper.verify(str(password), str(user.password)):
            return "Invalid Credentials"
        
        return  "welcome"
        
            

# Define GraphQL schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQL(schema=schema)
# Add Strawberry GraphQL app to FastAPI
# @router.post("/graphql")
# async def graphql(request: strawberry.asgi.Request):
#     return await strawberry.asgi.graphql(request, schema)
router.add_route('/graphql',graphql_app )