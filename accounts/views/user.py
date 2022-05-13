from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse

from accounts.services import get_password_hash, generate_random_password
from accounts.schemas import CreateUser, ResponseUser, UpdatedUser, User
from accounts.messages import USER_CREATED
from accounts.views.current_user import get_current_user
from settings import settings


router = APIRouter()

tags = ["accounts"]


@router.post(
    "/v1/create-user", tags=tags, responses={201: {"model": ResponseUser}}
)
async def add_new_user(request: Request, user: CreateUser):
    """Создание нового пользователя"""
    try:
        await request.app.db.create_user(
            first_name=user.first_name,
            last_name=user.last_name,
            password=get_password_hash(generate_random_password()),
            phone_number=user.phone_number,
            email=user.email,
        )
        return ResponseUser(status_code=201, description=USER_CREATED)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")


@router.post("/v1/update-user", tags=tags)
async def update_user(
    request: Request,
    user: UpdatedUser,
    current_user: User = Depends(get_current_user),
):
    """Изменение информации о пользователе"""
    try:
        await request.app.db.update_user(
            user.user_id,
            user.first_name,
            user.second_name,
            user.username,
            user.password,
            user.email,
        )
        return ResponseUser(
            status_code=200, description="Данные успешно изменены"
        )
    except Exception as e:
        print(e)  # TODO логирование
