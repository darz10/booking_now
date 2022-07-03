from passlib.context import CryptContext
import random
import string


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def clear_phone(phone: str) -> str:
    """
    Очищаем телефон от посторонних символов.
    """
    new_phone = filter(str.isdigit, phone)
    return "".join(new_phone)


def get_password_hash(password: str):
    """
    Создание хэша пароля
    """
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """
    Проверка пароля
    """
    return password_context.verify(plain_password, hashed_password)


def generate_random_password() -> str:
    """
    Создание случайного пароля
    """
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
