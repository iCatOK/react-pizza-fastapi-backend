from pydantic import BaseModel
from database.models.user import User as DbUser


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None
    addresses: list[str] | None = None

    @classmethod
    def from_db_model(cls, model: DbUser):
        user = cls(username=model.username, full_name=model.full_name)
        user.addresses = [] if not model.addresses else [a.address for a in model.addresses]
        return user


class UserInDB(User):
    hashed_password: str