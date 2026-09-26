"""Auth routes: login (sets httpOnly session cookie), me, logout."""

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel

from lib.auth import create_session, destroy_session, require_user, verify_password
from lib.db import db
from models.auth import LoginRequest, User

router = APIRouter(prefix="/auth", tags=["auth"])


class OkResponse(BaseModel):
    ok: bool = True


@router.post("/login", response_model=User)
async def login(body: LoginRequest, response: Response):
    user = await db.users.find_one({"username": body.username}, {"_id": 0})
    if not user or not verify_password(body.password, user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Username atau password salah")
    await create_session(user["id"], response)
    user.pop("password_hash", None)
    return User(**user)


@router.get("/me", response_model=User)
async def me(user: dict = Depends(require_user)):
    return User(**user)


@router.post("/logout", response_model=OkResponse)
async def logout(request: Request, response: Response):
    await destroy_session(request, response)
    return OkResponse()
