from datetime import datetime, timedelta, timezone
from typing import Annotated

from database.models import User
from dependencies import get_async_session

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



