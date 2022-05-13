from fastapi import Request, HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.models import OAuthFlows
from fastapi.security.oauth2 import SecurityScopes
from pydantic import ValidationError
from jose import jwt, JWTError
from accounts.messages import COULD_NOT_VALIDATE, NO_PERMISSIONS
from settings import Settings, settings, get_settings


ACCESS_TOKEN_EXPIRE_DAYS = 365 * 5
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/login")


async def get_current_user(
    request: Request,
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    settings: Settings = Depends(get_settings),
):
    if security_scopes.scopes:
        auth_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        auth_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=401,
        detail=COULD_NOT_VALIDATE,
        headers={"WWW-Authenticate": auth_value},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[ALGORITHM]
        )
        phone: str = payload.get("sub")
        if phone is None:
            raise credentials_exception
    except (ValidationError, JWTError):
        raise credentials_exception

    user = await request.app.db.get_user(phone_number=phone)

    if user is None:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in user.scopes:
            raise HTTPException(
                status_code=403,
                detail=NO_PERMISSIONS,
                headers={"WWW-Authenticate": auth_value},
            )
    return user
