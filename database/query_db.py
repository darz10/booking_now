from asyncpg import create_pool

from settings import settings


pool = None


class BookingDataBase:
    """Класс отвечающий за запросы к бд"""

    def __init__(self, psql_conn):
        self.psql_conn = psql_conn

    async def get_asyncpg_pool(self):
        global pool
        if pool is None:
            pool = await create_pool(self.psql_conn, max_size=90)
        return pool

    async def get_user(self, phone_number: int):
        """Получение данных о пользователе по номеру телефона"""
        db = await self.get_asyncpg_pool()
        async with db.acquire() as c:
            return await c.fetchrow(
                """
                SELECT id, first_name, last_name, phone_number, email, is_active, role_id 
                FROM users
                WHERE phone_number = $1
                """,
                phone_number,
            )

    async def create_user(
        self,
        first_name: str,
        last_name: str,
        password: str,
        phone_number: int,
        email: str,
        is_active: bool = True,
    ):
        """Создание пользователя"""
        db = await self.get_asyncpg_pool()
        async with db.acquire() as c:
            return await c.execute(
                """
                INSERT INTO users(first_name, last_name, password, phone_number, email, is_active, role_id)
                VALUES ($1, $2, $3, $4, $5, $6, $7);
                """,
                first_name,
                last_name,
                password,
                str(phone_number),
                email,
                is_active,
                settings.USER_DEFAULT_ROLE,
            )

    async def update_user(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
        password: str,
        phone_number: int,
        email: str,
        is_active: bool = True,
        role_id: int = settings.USER_DEFAULT_ROLE,
    ):
        """Обновление пользователя"""
        db = await self.get_asyncpg_pool()
        async with db.acquire() as c:
            return await c.execute(
                """
                UPDATE users
                SET first_name = $1, 
                    last_name = $2, 
                    password = $3, 
                    phone_number = $4, 
                    email = $5, 
                    is_active =$6, 
                    role_id = $7
                WHERE user_id = $8;
                """,
                first_name,
                last_name,
                password,
                str(phone_number),
                email,
                is_active,
                role_id,
                user_id,
            )
