from database.datacoonect import db

class DictionaryFileId:
    """Хранит количесвто задач по физики"""

    def __init__(self):
        self.dictionary_phy = {}
        self.dictionary_inf = {}

    async def create_container_phy(self):
        for i in range(1, 21):
            if not i == 17:
                des = {index : value for index, value in enumerate(await db.get_task_phy(i))}
                self.dictionary_phy[i] = des

    async def create_container_inf(self):
        for i in range(1, 11):
            des = {index : value for index, value in enumerate(await db.get_task_inf(i))}
            self.dictionary_inf[i] = des

    async def get_item_phy(self, task_number, task_count):
        return self.dictionary_phy[task_number][task_count]
    
    async def get_item_inf(self, task_number, task_count):
        return self.dictionary_inf[task_number][task_count]

container_fileid = DictionaryFileId()