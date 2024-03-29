from aiomysql import Error
import aiomysql
from aiomysql import Connection

import asyncio
from asyncio.events import AbstractEventLoop

import sys 

from log import logger

from datetime import datetime
from config import Config, load_config


loop: AbstractEventLoop = asyncio.get_event_loop()
config: Config = load_config()

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DataBase(metaclass=Singleton):

    def __init__(self, host, port, user, password, database_name, loop) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database_name = database_name
        self.loop = loop
        self.conn = None

    async def connect(self): 
        """Функция созданий соеденении с базой данных"""
        try:
            if not self.conn:
                self.conn = await aiomysql.connect(
                                            host=self.host,
                                            port=self.port,
                                            user=self.user,
                                            password=self.password,
                                            db=self.database_name,
                                            autocommit=True,
                                            loop=self.loop)
        except Error as e:
            logger.error(f'CONNECTION ERROR: {e}')
            sys.exit(1)
        else:
            logger.info('CONNECTION SUCCESSFULL')

    async def add_user(self, 
                       user_id: int|str,
                       username: str,
                       full_name: str
                       )-> None:
        """
        Функция добовляет новых пользователей в БД
        :param user_id: id пользователя
        :param username: Имя пользователя 
        :param full_name: first name + last_name
        """
        pool: Connection = self.conn
        async with pool.cursor() as cur:
            await cur.execute(f"INSERT INTO users.users (users_id, url, full_name) VALUES(%s, %s, %s)", (str(user_id), username, full_name))
            await cur.execute(f"INSERT INTO users.physics_task_users (users_id) VALUES(%s)", (str(user_id)))
            await cur.execute(f"INSERT INTO users.informatics_task_users (users_id) VALUES(%s)", (str(user_id)))

    async def count_task(self, 
                        task_number: int|str, 
                        objekt: str
                        )-> int:
        """
        Функция определяет количестов file_id в ..._task
        :param task_number: Номер задачи 
        :param objekt: informatics or physics
        :return: количество занчений в столбце
        """
        pool: Connection = self.conn
        async with pool.cursor() as cursor:
            await cursor.execute(f"SELECT COUNT(task_{task_number}) FROM users.{objekt}_task")
            for row in await cursor.fetchall():
                return row[0]

    async def count_user(self, user_id: int|str)-> int:
        """
        Функция проверка есть ли пользователь в базе данных
        :param user_id: user_id
        :return: 0 or 1 
        """
        pool: Connection = self.conn
        async with pool.cursor() as cursor:
            await cursor.execute(f"SELECT 1 FROM users.users WHERE users_id = '{user_id}' LIMIT 1")
            for row in await cursor.fetchall():
                return row[0]       

    async def update_user_task(self, 
                               user_id: int|str, 
                               object: str, 
                               task_number: int|str, 
                               sign: str
                               )-> int:
        """
        Функция обновление данных в таблице ..._task_users
        :param user_id: id пользователя
        :param objekt: informatics or physics
        :param task_number: Номер задачи 
        :param sign: '-' or '+'
        :return: количество занчений в столбце
        """
        pool: Connection = self.conn
        async with pool.cursor() as cur:
            await cur.execute(f"UPDATE users.{object}_task_users SET task_{task_number} = task_{task_number} {sign} 1 WHERE users_id = '{user_id}'")

    async def chek_count(self, 
                         user_id: int|str, 
                         object: str, 
                         task_number: int|str
                         )-> int:
        """
        Выводит число, которое обозначает на какой задаче остановился пользователь
        :param user_id: id пользователя
        :param objekt: informatics or physics
        :param task_number: Номер задачи
        :return: int столбца task_n
        """
        pool: Connection = self.conn
        async with pool.cursor() as cur:
            await cur.execute(f"SELECT users_id, task_{task_number} FROM users.{object}_task_users WHERE (users_id) = ({user_id})")
            for row in await cur.fetchall():
                return row[1]

    async def get_task_decision(self, 
                                user_id: int|str, 
                                object: str, 
                                task_number: int|str
                                )-> str:
        """Функция выдаёт решение задачи
        :param user_id: id пользователя
        :param objekt: informatics or physics
        :param task_number: Номер задачи
        :return: file_id or str
        """
        pool: Connection = self.conn
        async with pool.cursor() as cur:
            await cur.execute(f"SELECT id, task_{task_number} FROM users.{object}_task_decision WHERE (id) = ({user_id})")
            for row in await cur.fetchall():
                return row[1]

    async def get_task_phy(self, task_number: str)-> str:
        """
        Функция выдаёт file_id задачи по физике
        :param task_number: Номер задачи
        :return: file_id physics_task
        """
        pool: Connection = self.conn
        res = []
        async with pool.cursor() as cur:
            await cur.execute(f"SELECT task_{task_number} FROM users.physics_task;")
            for row in await cur.fetchall():#Сопрограмма возвращает все строки результирующего набора запроса -> (list[tuple(),])
                if row[0]:#if list[none] если столбец пустой, то не добовляем в массив
                    res.append(row[0])
            return res
        
    async def get_task_inf(self, task_number: str)-> list:
        """
        Функция выдаёт id задачи по информатике
        :param task_number: Номер задачи
        :return: list
        """
        pool: Connection = self.conn
        res = []
        async with pool.cursor() as cur:
            await cur.execute(f"SELECT task_{task_number} FROM users.informatics_task;")
            for row in await cur.fetchall():#Сопрограмма возвращает все строки результирующего набора запроса -> (list[tuple(),])
                if row[0]:#if list[none] если столбец пустой, то не добовляем в массив
                    res.append(row[0])
            return res
            
    async def add_log(self,  
                      user_id:int , 
                      content:str)-> None:
        """
        Функция для логирования
        Функция выдаёт id задачи по информатике
        :param user_id: Уникальный идентификатор для этого пользователя
        :param telegram_object: Объект телеграмма
        :param content: content
        :return: list
        """
        pool: Connection = self.conn
        async with pool.cursor() as cur:
            await cur.execute(f"INSERT INTO users.logs (user_id, content)\
                              VALUES(%s, %s)", (str(user_id),content))

    async def get_data(self, 
                       user_id: int|str) -> datetime:
        """
        Выводит дату регестрациии пользователя
        """
        pool: Connection = self.conn
        async with pool.cursor() as cur:
            await cur.execute(f"SELECT users_id, data  FROM users.users WHERE users_id = {user_id}")
            for row in await cur.fetchall():
                return row[1]

    async def get_task_users(self, 
                             user_id: int|str, 
                             object: str
                             )-> list:
        """
        Функция выводит с таблицы _task_users по id все числа
        :param user_id: id пользователя
        :param objekt: informatics or physics
        """
        pool: Connection = self.conn
        async with pool.cursor() as cur:
            await cur.execute(f"SELECT * FROM users.{object}_task_users WHERE users_id = {user_id}")
            for row in await cur.fetchall():
                return row[1:]#row -> tuple() row[0] -> user_id 
    
    async def count_user_for_admin(self)-> int:
        """Количество пользователей"""
        pool: Connection = self.conn
        async with pool.cursor() as cur:
            await cur.execute("SELECT count(*) FROM users.users")
            for row in await cur.fetchall():
                return row[0]

            
db = DataBase(
    host=config.bd_bot.host,
    port=config.bd_bot.port,
    user=config.bd_bot.user,
    password=config.bd_bot.password,
    database_name=config.bd_bot.database_name,
    loop=loop)