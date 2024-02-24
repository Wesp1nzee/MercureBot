from lexicon.dict_task_number import container

class ContainerCache:
    def __init__(self):
        self.dictionary = {}

    def create_cache(self):
        for i in range(1, 11):
            self.inner_dict = { j : False for j in range(1, container.get_item(i)+1)}
            self.dictionary[i] = self.inner_dict
    
    async def check_key(self, key_1, key_2):
        return self.dictionary[key_1][key_2]

    async def update_val(self, key_1, key_2, val):
        self.dictionary[key_1][key_2] = val
        

cache = ContainerCache()

