import aiomysql
import sys 
from database.setting import settings
from aiomysql import Error
import logging

class DataBase:
    @staticmethod
    async def create_connection(HOST, PORT, USER, PASSWORD, DATABASE, loop): 
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

    @staticmethod
    async def add_user(id, name):
        """Функция добовляет новых пользователей в базу данных"""
        pool = settings.conn
        async with pool.cursor() as cur:
            await cur.execute(f"INSERT INTO users.users VALUES({id},'{name}')")

    @staticmethod
    async def count_user(id):
        """Функция проверка есть ли пользователь в базе данных"""
        pool = settings.conn
        async with pool.cursor() as cursor:
            await cursor.execute(f"SELECT COUNT(*) FROM users.users WHERE ID = {id} ")
            for row in await cursor.fetchall():
                return row[0]
        

db = DataBase()