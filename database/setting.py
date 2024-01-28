class Settings:
    def __init__(self):
        self._conn = None

    @property
    def conn(self):
        return self._conn

    @conn.setter
    def conn(self, value):
        self._conn = value


settings = Settings()
