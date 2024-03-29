from database.datacoonect import db

class DictionaryFileId:
    """Хранит количесвто задач по физики"""

    dictionary_phy:dict = {}
    dictionary_inf:dict = {}

    async def create_container_fileId(self):
        """Создаёт словари в которых [Номер задачи : [номер задачи по счету : fileId]]"""
        for i in range(1, 21):
            if not i in [17, 18]:
                des = {index+1 : value for index, value in enumerate(await db.get_task_phy(i))}
                self.dictionary_phy[str(i)] = des
            else: 
                if i == 18:
                    for g in range(1,4):
                        des = {index+1 : value for index, value in enumerate(await db.get_task_phy(f"18_{g}"))}
                        self.dictionary_phy[f'18_{g}'] = des

        for i in range(1, 11):
            des = {index+1 : value for index, value in enumerate(await db.get_task_inf(i))}
            self.dictionary_inf[str(i)] = des

    async def get_item_phy(self, task_number, task_count)-> str:
        """Получаем file_id задачи по физики"""
        return self.dictionary_phy[task_number][task_count]
    
    async def get_item_inf(self, task_number, task_count)-> str:
        """Получаем file_id задачи по информатики"""
        return self.dictionary_inf[task_number][task_count]

container_fileid = DictionaryFileId()