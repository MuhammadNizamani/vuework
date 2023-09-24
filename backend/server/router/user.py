from server.models.models import Users, session
from fastapi.routing import APIRouter
router = APIRouter(prefix="/users", tags=["User  Router"])
@router.get("/data/{user_id}")
def get_user(user_id:int):
    user = session.query(Users).filter(Users.user_id == user_id).first()
    return user