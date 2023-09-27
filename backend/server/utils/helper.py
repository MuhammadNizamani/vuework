from passlib.context import CryptContext
import logging
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str)-> str:
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    try:
        # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        result = pwd_context.verify(plain_password, hashed_password)
        return result
    except Exception as e:
        logging.error(f"Error verifying password: {e}")
        return False

    