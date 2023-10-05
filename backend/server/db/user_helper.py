 # Working on rating system 
from server.schemas import users_schemas
from server.models.models import Users, session, Rating
from server.utils import chessdotcomapi
 
def add_rating(user_id:int) -> users_schemas.RatingType:
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
        