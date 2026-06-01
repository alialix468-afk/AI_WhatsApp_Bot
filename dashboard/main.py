from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session as SQLAlchemySession
from database.models import User, Message, Setting
from database import get_db
from shared import get_current_user, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, UserInDB, personality_service, memory_service
from datetime import timedelta

router = APIRouter()
templates = Jinja2Templates(directory="dashboard/templates")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "title": "تسجيل الدخول"})

@router.post("/token")
async def login_for_access_token(request: Request, db: SQLAlchemySession = Depends(get_db)):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")
    user = await authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@router.get("/", response_class=HTMLResponse)
async def dashboard_home(request: Request, current_user: UserInDB = Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request, "title": "لوحة تحكم AI WhatsApp Assistant", "current_user": current_user})

@router.get("/settings", response_class=HTMLResponse)
async def dashboard_settings(request: Request, current_user: UserInDB = Depends(get_current_user)):
    # Fetch user-specific settings or global settings
    # For now, just pass a placeholder
    personalities = personality_service.list_personalities()
    current_personality = memory_service.get_preference(db, current_user.id, "personality", "friendly")
    return templates.TemplateResponse("settings.html", {"request": request, "title": "الإعدادات", "current_user": current_user, "personalities": personalities, "current_personality": current_personality})

@router.post("/settings")
async def update_settings(request: Request, current_user: UserInDB = Depends(get_current_user), db: SQLAlchemySession = Depends(get_db)):
    form = await request.form()
    new_personality = form.get("personality")
    if new_personality and new_personality in personality_service.list_personalities():
        memory_service.update_preference(db, current_user.id, "personality", new_personality)
        return RedirectResponse(url="/dashboard/settings", status_code=status.HTTP_302_FOUND)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid personality selected")

@router.get("/users", response_class=HTMLResponse)
async def dashboard_users(request: Request, current_user: UserInDB = Depends(get_current_user), db: SQLAlchemySession = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("users.html", {"request": request, "title": "المستخدمون", "current_user": current_user, "users": users})
