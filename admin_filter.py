from aiogram.filters import BaseFilter
from aiogram.types import Message
from config import Config, load_config

config: Config = load_config()

class IsAdmin(BaseFilter):

    admin_ids: int = config.tg_bot.admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == self.admin_ids
    

AdminFilter = IsAdmin()