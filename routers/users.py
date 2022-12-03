from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, status, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from models.auth import User, UserInDB, Token, TokenData
from database.config import async_session
from database.repositories import UserRepository
from database.models.user import User as DbUser
from exceptions.exceptions import AuthExceptions


SECRET_KEY = "6e372d3ab814222da7e862d434ad91d38ae28c73c3fbb8c05341fcfbdde34c2c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(username: str):
    async with async_session() as session:
        async with session.begin():
            user_repo = UserRepository(session)
            return await user_repo.get_user_by_username(username)


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user or verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> DbUser:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise AuthExceptions.credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise AuthExceptions.credentials_exception
    db_user: DbUser  = await get_user(username=token_data.username)
    if db_user is None:
        raise AuthExceptions.credentials_exception
    out_user: User = User.from_db_model(db_user)
    return out_user

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise AuthExceptions.unauthorized_exception
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users")
async def register_user(username: str, password: str, full_name: str):
    hashed_password = pwd_context.hash(password, 'bcrypt')
    async with async_session() as session:
        async with session.begin():
            user_repo = UserRepository(session)
            return await user_repo.create_user(username, hashed_password, full_name)


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]