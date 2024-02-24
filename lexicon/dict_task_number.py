from database.datacoonect import db

class DictionaryContainer:
    def __init__(self):
        self.dictionary = {}

    async def create_container(self):
        for i in range(1,11):
            self.dictionary[i] = await db.count_task(i)

    def get_item(self, key):
        return self.dictionary.get(key)

container = DictionaryContainer()

