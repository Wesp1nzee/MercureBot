from aiomysql import Error
import aiomysql

import sys 

from database.setting import settings
from config import HOST, USER, PASSWORD, DATABASE, PORT


class DataBase:
    
    async def create_connection(self,loop): 
        """Функция созданий соеденении с базой данных"""
        if not settings.conn:
            try:
                # Создаем соеденение
                settings.conn = await aiomysql.connect(
                                            host=HOST,
                                            port=PORT,
                                            user=USER,
                                            password=PASSWORD,
                                            db=DATABASE,
                                            autocommit=True,
                                            loop=loop)
            except Error as e:
                print(f'CONNECTION ERROR: {e}')
                sys.exit(1)
            else:
                print('CONNECTION SUCCESSFULL')

    async def add_user(self, id, name):
        """Функция добовляет новых пользователей в базу данных"""
        pool = settings.conn
        async with pool.cursor() as cur:
            await cur.execute(f"INSERT INTO users.users (users_id, name) VALUES({id},'{name}')")
            await cur.execute(f"INSERT INTO users.physics_task_users (users_id) VALUES('{id}')")
            await cur.execute(f"INSERT INTO users.informatics_task_users (users_id) VALUES('{id}')")

    async def count_user(self, id)-> int:
        """Функция проверка есть ли пользователь в базе данных"""
        pool = settings.conn
        async with pool.cursor() as cursor:
            await cursor.execute(f"SELECT COUNT(*) FROM users.users WHERE users_id = {id} ")
            for row in await cursor.fetchall():
                return row[0]
            
    async def update_user_task(self, id, object, task_number, sign)-> int:
        """Функция обновление данных в таблице task"""
        pool = settings.conn
        async with pool.cursor() as cur:
            await cur.execute(f"UPDATE users.{object}_task_users SET task_{task_number} = task_{task_number} {sign} 1 WHERE users_id = '{id}'")

    async def chek_count(self, id, object, task_number)-> int:
        """Функция счетчик задач"""
        pool = settings.conn
        async with pool.cursor() as cur:
            await cur.execute(f"SELECT users_id, task_{task_number} FROM users.{object}_task_users WHERE (users_id) = ({id})")
            for row in await cur.fetchall():
                return row[1]


db = DataBase()