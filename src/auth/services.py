from datetime import datetime, timezone, timedelta
import jwt
from jwt.exceptions import PyJWTError
from passlib.context import CryptContext
from config import settings
from database.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from auth.schemas import UserSchema, TokenSchema, UserRegisterSchema, UserRole
from src.auth.repositories import UserRepository
from fastapi.exceptions import HTTPException
from fastapi import status
from utils import pwd_context

ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


class TokenManager():

    def decode_jwt(self,
                   token: str | bytes,
                   public_ley: str = settings.auth_jwt.public_key_path.read_text(),
                   algorithm: str = settings.auth_jwt.algorithm
                   ):
        decoded = jwt.decode(
            token,
            public_ley,
            algorithms=[algorithm],
            options={"verify_exp": False}
        )
        return decoded

    def encode_jwt(self,
                   payload: dict,
                   private_key: str = settings.auth_jwt.private_key_path.read_text(),
                   algorithm: str = settings.auth_jwt.algorithm,
                   expire_timedelta: timedelta | None = None,
                   expire_minutes: int = settings.auth_jwt.access_token_expire_minutes
                   ):
        to_encode = payload.copy()
        now = datetime.now(timezone.utc)
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)

        to_encode.update(
            exp=expire,
            iat=now,
        )
        encoded = jwt.encode(
            to_encode,
            private_key,
            algorithm=algorithm
        )
        return encoded

    def create_token(self, data: dict,
                     token_type: str
                     ) -> str:
        to_encode = data.copy()
        expire_timedelta = None
        if token_type == ACCESS_TOKEN_TYPE:

            to_encode.update({"type": "access"})
        elif token_type == REFRESH_TOKEN_TYPE:
            to_encode.update({"type": "refresh"})
            expire_timedelta = timedelta(days=settings.auth_jwt.refresh_token_expire_days)

        return self.encode_jwt(payload=to_encode, expire_timedelta=expire_timedelta)


class AuthService:

    def __init__(self, session):
        self.user_repository = UserRepository(session)
        self.token_manager = TokenManager()

    async def add_user(
            self, user: UserRegisterSchema
    ):
        existing_user = await self.user_repository.get_user(user.email.__str__())
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Email already exists")
        hashed_password = get_password_hash(user.password)
        user = await self.user_repository.add_user(
            username=user.username,
            password=hashed_password,
            phone_number=user.phone_number,
            email=user.email,
        )
        access_token = self.token_manager.create_token({"sub": user.email}, token_type=ACCESS_TOKEN_TYPE)
        refresh_token = self.token_manager.create_token({"sub": user.email}, token_type=REFRESH_TOKEN_TYPE)

        result = {
            "tokens": TokenSchema(access_token=access_token,
                                  refresh_token=refresh_token),
            "role": UserRole(role=user.role)
        }

        return result

    async def login_user(
            self, email_address, password
    ):
        user = await self.user_repository.get_user(email_address)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )

        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )

        access_token = self.token_manager.create_token({"sub": user.email}, token_type=ACCESS_TOKEN_TYPE)
        refresh_token = self.token_manager.create_token({"sub": user.email}, token_type=REFRESH_TOKEN_TYPE)
        result = {
            "tokens": TokenSchema(access_token=access_token,
                                  refresh_token=refresh_token),
            "role": UserRole(role=user.role)
        }

        return result

    async def refresh_token(
            self,
            refresh_token: str
    ) -> TokenSchema:
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token is missing"
            )

        try:
            payload = self.token_manager.decode_jwt(refresh_token)
        except PyJWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid refresh token {e}"
            )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token type"
            )

        expire = payload.get('exp')
        if not expire:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expiration not found"
            )

        if expire < int(datetime.now(timezone.utc).now().timestamp()):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired"
            )

        user_email_address = payload.get("sub")
        if not user_email_address:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        existing_user = await self.user_repository.get_user(email=user_email_address)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        access_token = self.token_manager.create_token({"sub": existing_user.email}, token_type=ACCESS_TOKEN_TYPE)

        return TokenSchema(access_token=access_token)

    async def get_user(self, email) -> User:
        existing_user = await self.user_repository.get_user(email=email)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        return existing_user
