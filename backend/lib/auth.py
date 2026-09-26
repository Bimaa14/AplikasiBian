"""Session auth: httpOnly cookie + server-side session docs in Mongo. Frontend never sees a token."""

import uuid
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, Request, Response
from passlib.context import CryptContext

from lib.db import db

SESSION_COOKIE = "bengkel_session"
SESSION_TTL = timedelta(days=7)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return pwd_context.verify(password, password_hash)
    except Exception:
        return False


async def create_session(user_id: str, response: Response) -> None:
    token = uuid.uuid4().hex + uuid.uuid4().hex
    expires_at = datetime.now(timezone.utc) + SESSION_TTL
    await db.sessions.insert_one(
        {"token": token, "user_id": user_id, "expires_at": expires_at}
    )
    response.set_cookie(
        key=SESSION_COOKIE,
        value=token,
        httponly=True,
        samesite="lax",
        path="/",
        max_age=int(SESSION_TTL.total_seconds()),
    )


async def destroy_session(request: Request, response: Response) -> None:
    token = request.cookies.get(SESSION_COOKIE)
    if token:
        await db.sessions.delete_one({"token": token})
    response.delete_cookie(key=SESSION_COOKIE, path="/")


async def require_user(request: Request) -> dict:
    """FastAPI dependency: 401 unless a live session cookie resolves to a user."""
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        raise HTTPException(status_code=401, detail="Belum login")
    session = await db.sessions.find_one({"token": token}, {"_id": 0})
    if not session:
        raise HTTPException(status_code=401, detail="Sesi tidak valid, silakan login")
    expires_at = session.get("expires_at")
    if expires_at is not None:
        # motor hands back naive datetimes — normalise before comparing (aware vs naive raises)
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Sesi berakhir, silakan login kembali")
    user = await db.users.find_one({"id": session["user_id"]}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=401, detail="Pengguna tidak ditemukan")
    user.pop("password_hash", None)
    return user
