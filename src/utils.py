
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
from datetime import datetime

MONTHS_RU = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августа",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря"
}

def format_event_dates(start: datetime, end: datetime) -> str:
    start_day, start_month, start_year = start.day, start.month, start.year
    end_day, end_month, end_year = end.day, end.month, end.year

    def format_month(month_num):
        return MONTHS_RU.get(month_num, str(month_num))

    def format_single_date(dt):
        return f"{dt.day} {format_month(dt.month)} {dt.year}"

    if start.date() == end.date():
        return f"{format_single_date(start)} г."

    if start_year == end_year:
        if start_month == end_month:
            return f"{start_day} – {end_day} {format_month(start_month)} {start_year} г."
        else:
            return f"{start_day} {format_month(start_month)} – {end_day} {format_month(end_month)} {start_year} г."
    else:
        return f"{format_single_date(start)} – {format_single_date(end)} г."



