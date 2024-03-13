from aiomysql import Error
import aiomysql

import sys 

from config import HOST, USER, PASSWORD, DATABASE, PORT


class DataBase:
    
    async def create_connection(self,loop): 
        """Функция созданий соеденении с базой данных"""
        try:
            # Создаем соеденение
            self.conn = await aiomysql.connect(
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

    async def add_user(self, id, url, full_name):
        """Функция добовляет новых пользователей в базу данных"""
        pool = self.conn
        async with pool.cursor() as cur:
            await cur.execute(f"INSERT INTO users.users (users_id, url, full_name) VALUES({id}, '{url}', '{full_name}')")
            await cur.execute(f"INSERT INTO users.physics_task_users (users_id) VALUES('{id}')")
            await cur.execute(f"INSERT INTO users.informatics_task_users (users_id) VALUES('{id}')")

    async def count_task(self, task_number, objekt)-> int:
        """Функция количесвто задач в бд"""
        pool = self.conn
        async with pool.cursor() as cursor:
            await cursor.execute(f"SELECT COUNT(task_{task_number}) FROM users.{objekt}_task")
            for row in await cursor.fetchall():
                return row[0]

    async def count_user(self, id)-> int:
        """Функция проверка есть ли пользователь в базе данных"""
        pool = self.conn
        async with pool.cursor() as cursor:
            await cursor.execute(f"SELECT 1 FROM users.users WHERE users_id = '{id}' LIMIT 1")
            for row in await cursor.fetchall():
                return row[0]       

    async def update_user_task(self, id, object, task_number, sign)-> int:
        """Функция обновление данных в таблице task"""
        pool = self.conn
        async with pool.cursor() as cur:
            await cur.execute(f"UPDATE users.{object}_task_users SET task_{task_number} = task_{task_number} {sign} 1 WHERE users_id = '{id}'")

    async def chek_count(self, id, object, task_number)-> int:
        """Функция счетчик задач"""
        pool = self.conn
        async with pool.cursor() as cur:
            await cur.execute(f"SELECT users_id, task_{task_number} FROM users.{object}_task_users WHERE (users_id) = ({id})")
            for row in await cur.fetchall():
                return row[1]

    async def get_task_decision(self, id, task_number, object)-> str:
        """Функция выдаёт решение задачи"""
        pool = self.conn
        async with pool.cursor() as cur:
            await cur.execute(f"SELECT id, task_{task_number} FROM users.{object}_task_decision WHERE (id) = ({id})")
            for row in await cur.fetchall():
                return row[1]

    async def get_task(self, object, id, task_number)-> str:
        """Функция выдаёт id задачи"""
        pool = self.conn
        async with pool.cursor() as cur:
            await cur.execute(f"SELECT id, task_{task_number} FROM users.{object}_task WHERE (id) = ({id})")
            for row in await cur.fetchall():
                return row[1]
            
    async def add_log(self, chat_id:int , user_id:int , user_full_name:str, telegram_object:str, content:str):
        """Функция для логирования"""
        pool = self.conn
        async with pool.cursor() as cur:
            await cur.execute(f"INSERT INTO users.logs (chat_id, user_id, user_full_name, telegram_object, content)\
                              VALUES('{chat_id}', '{user_id}', '{user_full_name}', '{telegram_object}', '{content}')")
    
    async def suumme(self, id, object):
        """Функция выводит с таблицы _task_users по id все числа"""
        pool = self.conn
        async with pool.cursor() as cur:
            await cur.execute(f"SELECT * FROM users.{object}_task_users WHERE users_id = {id}")
            for row in await cur.fetchall():
                return row[1:]

            
db = DataBase()