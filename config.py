from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str       
    admin_ids: int  

@dataclass
class DateBase:
    host: str
    port: int  
    user: str
    password: str
    database_name: str

@dataclass
class Config:
    tg_bot: TgBot
    bd_bot: DateBase

# Создаем функцию, которая будет читать файл .env и возвращать
# экземпляр класса Config с заполненными полями token и admin_ids
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=env.int('ADMIN_IDS')
        ),
        bd_bot=DateBase(
            host=env('HOST'),
            port=env.int('PORT'),
            user=env('USER'),
            password=env('PASSWORD'),
            database_name=env('DATABASE_NAME')
        )
    )