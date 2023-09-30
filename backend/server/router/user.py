import strawberry
from server.models.models import Users, session, Rating
from fastapi.routing import APIRouter, Response
from fastapi import HTTPException, status
from server.schemas.users_schemas import UserInput, UserType, SignUpResult, LoginResult, LoginType, RatingType
import typing
from server.utils import helper, exception, chessdotcomapi
import datetime


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
    @strawberry.field
    def login_user(self ,email:str, password: str) -> LoginResult:
        
        user = session.query(Users).filter(Users.email == email).first()
        if user is None:
            return LoginResult(success=False, login=None, message= "Invalid Credentials")  
        # print(str(user.password))
        if not helper.verify(str(password), str(user.password)):
            return LoginResult(success=False, login=None, message= "Invalid Credentials") 
        
        return  LoginResult(success=False, login=LoginType(user_id=user.user_id,
                                                           name =user.name,
                                                           email=user.email,
                                                           chess_username=user.chess_username,
                                                           avater=user.avatar,
                                                           last_online= user.last_online,
                                                           league= user.league,
                                                           country= user.country,
                                                           followers = user.followers,
                                                           player_id= user.player_id,
                                                           status= user.status,
                                                           is_streamer= user.is_streamer,
                                                           verified= user.verified)
                            , message= "Login successfully! Welcome ")
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, info,user_input: UserInput) -> SignUpResult:
        
        # hashing the passward 
        hashed_password = helper.hash(user_input.password)
        user_input.password = hashed_password
        
        # Getting data from chess.com 
        data = chessdotcomapi.get_data_from_chessdotcom(player=user_input.chess_username)
        if '404' in data:
            return SignUpResult(success=False,user=None, message="You chess.com username does not exit") 
            
        
        # Checking that avatar (profile pic  ) of user is upload or not 
        # Checking this important becasue if there is not avatar then chess.com won't retrun avater field in the data
        if 'avatar' in data:
            new_user = Users(name = user_input.name, 
                            chess_username= user_input.chess_username, email=user_input.email,
                            password = user_input.password, avatar= data['avatar'], 
                            player_id = data['player_id'], url = data['url'], followers = data['followers'],
                            country= data['country'], 
                            last_online =datetime.datetime.fromtimestamp(data['last_online']),
                            joined=datetime.datetime.fromtimestamp(data['joined']) ,
                            status = data['status'], is_streamer= data['is_streamer'], verified= data['verified'],
                            league= data['league'] )
        else:
            new_user = Users(name = user_input.name, 
                            chess_username= user_input.chess_username, email=user_input.email,
                            password = user_input.password, 
                            avatar= "https://www.chess.com/bundles/web/images/user-image.007dad08.svg", 
                            player_id = data['player_id'], url = data['url'], followers = data['followers'],
                            country= data['country'], 
                            last_online =datetime.datetime.fromtimestamp(data['last_online']),
                            joined=datetime.datetime.fromtimestamp(data['joined']) ,
                            status = data['status'], is_streamer= data['is_streamer'], verified= data['verified'],
                            league= data['league'] )
            
        # new_user = Users(**user_input.to_dict())
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return SignUpResult(success=True,user=UserType(user_id=new_user.user_id, 
                                                        name=new_user.name, 
                                                        email = new_user.email, 
                                                        chess_username=new_user.chess_username),
                            message="User created successfully")

    # UserType(**user_input.to_dict())
    # UserType(user_id=new_user.user_id, name=new_user.name, email = new_user.email, chess_username=new_user.chess_username)
    # UserType(name = new_user.name, email = new_user.email,chess_username= new_user.chess_username)

    @strawberry.mutation
    def update_user(self, info, id: int, name: str, email: str, chess_username:str, password: str) ->  str:
        user_query = session.query(Users).filter(Users.user_id == id)
        user = user_query.first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id: {id} does not exist",
            )

        user.name = name
        user.email = email
        user.chess_username = chess_username
        user.password = password
        session.commit()
        return user

    @strawberry.mutation
    def delete_user(self, info, id: int) -> str:
        try:
            user_query = session.query(Users).filter(Users.user_id == id)
            user = user_query.first()
            if user is None:
                return f"User with id: {id} does not exist"
                
            user_query.delete(synchronize_session=False)
            session.commit()
            return "User deleted successfully"
        except exception.UserDoesNotExist:
            return f"User with id: {id} does not exist"
    
    # Working on rating system 
    @strawberry.mutation
    def add_rating(self, info, user_id:int) -> RatingType:
        user_query = session.query(Users).filter(Users.user_id == user_id).first()
        data = chessdotcomapi.get_rating_data_from_chessdotcom(player=user_query.chess_username)
        if 'chess_blitz' in data:
            chess_blitz = int(data['chess_blitz']['last']['rating'])
        else:
            chess_blitz = None
        if 'chess_bullet' in data:
            chess_bullet = int(data['chess_bullet']['last']['rating'])
        else:
            chess_bullet = None
        if 'chess_daily' in data:
            chess_daily = int(data['chess_daily']['last']['rating'])
        else:
            chess_daily = None
        if 'chess_rapid' in data:
            chess_rapid = int(data['chess_rapid']['last']['rating'])
        else:
            chess_rapid= None
            
        rating = Rating(user_id = user_id, 
        daily_rating=chess_daily,
        rapid_rating = chess_rapid,
        blitz = chess_blitz, 
        bullet_rating= chess_bullet)
        session.add(rating)
        session.commit()
        session.refresh(rating)
        return RatingType(user_id=user_id, 
                          daily_rating=chess_daily, 
                          rapid_rating=chess_rapid, 
                          blitz=chess_blitz, 
                          bullet_rating=chess_bullet)
         
        
    
    
        
            

# Define GraphQL schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQL(schema=schema)
# Add Strawberry GraphQL app to FastAPI
# @router.post("/graphql")
# async def graphql(request: strawberry.asgi.Request):
#     return await strawberry.asgi.graphql(request, schema)
router.add_route('/graphql',graphql_app )