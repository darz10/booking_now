from firebase_admin import credentials, initialize_app, auth
from firebase_admin._auth_utils import InvalidIdTokenError
from settings import settings
from fastapi import HTTPException

from accounts.utils import clear_phone
from accounts.messages import FIREBASE_AUTH_INVALID_TOKEN


class FirebaseManager:
    """
    Класс интеграции с Firebase
    """

    @classmethod
    def get_phone_by_token(cls, firebase_token: str):
        """
        Получить номер телефона, верифицированный в рамках firebase Auth, по токену, переданному в метод
        """
        cred = credentials.Certificate(settings.FIREBASE_APP_CREDENTIALS)
        try:
            initialize_app(credential=cred)
        except ValueError:
            pass
        try:
            decoded_token = auth.verify_id_token(firebase_token)
        except InvalidIdTokenError:
            raise HTTPException(
                status_code=400, detail=FIREBASE_AUTH_INVALID_TOKEN
            )
        phone = decoded_token["firebase"]["identities"]["phone"][0]
        return clear_phone(phone)
