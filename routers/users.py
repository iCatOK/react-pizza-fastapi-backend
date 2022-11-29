from fastapi import APIRouter

SECRET_KEY = "6e372d3ab814222da7e862d434ad91d38ae28c73c3fbb8c05341fcfbdde34c2c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
    },
    "79273235411": {
        "username": "79273235411",
        "full_name": "Kamil Mambetov",
        "hashed_password": "$2b$12$YFeaCeA5OdRBVlY1ysUQq.UPGVl9W1burDBz/V2zfd1zxPZPDWcNm"
    }
}

router = APIRouter()


@router.get("/users/me/")
async def read_users_me():
    return fake_users_db["79273235411"]