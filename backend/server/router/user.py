import strawberry
from server.models.models import Users, session, Rating
from fastapi.routing import APIRouter, Response
from fastapi import HTTPException, status
from server.schemas import users_schemas
import typing
from server.utils import helper, exception, chessdotcomapi
import datetime
from typing import Dict

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
    def user(self, user_id: int) -> users_schemas.UserType or str:
        query = session.query(Users).filter(Users.user_id == user_id).first()
        return query

    @strawberry.field
    def users(self) -> typing.List[users_schemas.UserType]:
        return session.query(Users).all()
    # following method is for testing perpose 
    @strawberry.field
    def check_login_user(self ,email:str, password: str) -> str:
        
        user = session.query(Users).filter(Users.email == email).first()
        if user is None:
            return  "message: Invalid Credentials"
        # print(str(user.password))
        if not helper.verify(str(password), str(user.password)):
            return   "message: Invalid Credentials"
        
        return "token: your token"
    
    @strawberry.field
    def login_user(self ,email:str, password: str) -> users_schemas.LoginResult:
        
        user = session.query(Users).filter(Users.email == email).first()
        if user is None:
            return users_schemas.LoginResult(success=False, login=None, message= "Invalid Credentials")  
        # print(str(user.password))
        if not helper.verify(str(password), str(user.password)):
            return users_schemas.LoginResult(success=False, login=None, message= "Invalid Credentials") 
        
        return  users_schemas.LoginResult(success=False, login=users_schemas.LoginType(user_id=user.user_id,
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
    def create_user(self, info,user_input: users_schemas.UserInput) -> users_schemas.SignUpResult:
        
        # hashing the passward 
        hashed_password = helper.hash(user_input.password)
        user_input.password = hashed_password
        
        # Getting data from chess.com 
        data = chessdotcomapi.get_data_from_chessdotcom(player=user_input.chess_username)
        if '404' in data:
            return users_schemas.SignUpResult(success=False,user=None, message="You chess.com username does not exit") 
            
        
        # Checking that avatar (profile pic  ) of user is upload or not 
        # Checking this important becasue if there is not avatar then chess.com won't retrun avater field in the data
        if 'avatar' in data:
            avatar= data['avatar'], 
                            
        else:
           
            avatar= "https://www.chess.com/bundles/web/images/user-image.007dad08.svg", 
                           
                            
        # new_user = Users(**user_input.to_dict())
        new_user = Users(name = user_input.name, 
                            chess_username= user_input.chess_username, email=user_input.email,
                            password = user_input.password, avatar= avatar, 
                            player_id = data['player_id'], url = data['url'], followers = data['followers'],
                            country= data['country'], 
                            last_online =datetime.datetime.fromtimestamp(data['last_online']),
                            joined=datetime.datetime.fromtimestamp(data['joined']) ,
                            status = data['status'], is_streamer= data['is_streamer'], verified= data['verified'],
                            league= data['league'] )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return users_schemas.SignUpResult(success=True,user=users_schemas.UserType(user_id=new_user.user_id, 
                                                        name=new_user.name, 
                                                        email = new_user.email, 
                                                        chess_username=new_user.chess_username),
                            message="User created successfully")

    
    @strawberry.mutation
    def update_user(self, info, user_update:users_schemas.UserUpdateInput) -> users_schemas.UserUpdateResult:
        user_query = session.query(Users).filter(Users.user_id == user_update.user_id)
        user = user_query.first()
        if user is None:
            return users_schemas.UserUpdateResult(success=False, 
                                           update=None, 
                                           message= f"User with {user_update.user_id} does not exist ")

        user.name = user_update.name
        user.email = user_update.email
        user.avatar = user_update.avater
        user.player_id = user_update.player_id
        user.last_online = user_update.last_online
        user.league = user_update.league
        user.url = user_update.url
        user.country = user_update.country
        user.followers = user_update.followers
        user.status = user_update.status
        user.is_streamer = user_update.is_streamer
        user.verified = user_update.verified
        
        
        
        session.commit()
        return users_schemas.UserUpdateResult(success=True, 
                                           update=users_schemas.UserUpdateType(user_id=user_update.user_id,
                                                                               name = user.name,
                                                                               email=user.email,
                                                                               avater=user.avatar,
                                                                               player_id=user.player_id,
                                                                               last_online=user.last_online,
                                                                               league=user.league,
                                                                               url=user.url,
                                                                               country=user.country,
                                                                               followers=user.followers,
                                                                               status=user.status,
                                                                               is_streamer=user.is_streamer,
                                                                               verified=user.verified), 
                                           message= f"Updated successfully  ")

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
    def add_rating(self, info, user_id:int) -> users_schemas.RatingType:
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
        return users_schemas.RatingType(user_id=user_id, 
                          daily_rating=chess_daily, 
                          rapid_rating=chess_rapid, 
                          blitz=chess_blitz, 
                          bullet_rating=chess_bullet)
         
        
    
    
        
            

# Define GraphQL schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQL(schema=schema)
# Add Strawberry GraphQL app to FastAPI
router.add_route('/graphql',graphql_app )