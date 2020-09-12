import shelve

from hackabot.common.entities import UserInfo


class BaseStorage:
    def __init__(self, config):
        self._path = config['path']

    def set(self, key, value):
        with shelve.open(self._path) as storage:
            storage[str(key)] = value

    def get(self, key):
        with shelve.open(self._path) as storage:
            if str(key) in storage:
                return storage[str(key)]
            else:
                return None

    def delete(self, key):
        with shelve.open(self._path) as storage:
            if str(key) in storage:
                del storage[str(key)]


class GameStorage(BaseStorage):
    def __init__(self, config):
        super().__init__(config)

    def save_user_info(self, user: UserInfo):
        self.set(key=user.user_id, value=user)

    def get_user_info(self, user_id: int):
        self.get(key=user_id)

    def delete_user_info(self, user_id):
        self.delete(key=user_id)
