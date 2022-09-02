import copy
import typing

from aiogram.dispatcher.storage import BaseStorage
from sqlitedict import SqliteDict


class ChatDict(dict):
    def __init__(self, db: SqliteDict, chat: str):
        super().__init__(**db[chat])
        self.db = db
        self.chat = chat

    def commit(self):
        self.db[self.chat] = dict(**self)
        self.db.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()


class SqlLiteStorage(BaseStorage):
    def get_dict(self, chat) -> ChatDict:
        return ChatDict(self.db, chat)

    async def wait_closed(self):
        pass

    async def close(self):
        self.db.close()

    def __init__(self, filepath):
        self.db = SqliteDict(filepath)

    def resolve_address(self, chat, user):
        chat_id, user_id = map(str, self.check_address(chat=chat, user=user))

        if chat_id not in self.db:
            self.db[chat_id] = {}
        self.db.commit()
        if user_id not in self.db[chat_id]:
            with self.get_dict(chat_id) as chat_dict:
                chat_dict[user_id] = {'state': None, 'data': {}, 'bucket': {}}

        return chat_id, user_id

    async def get_state(self, *,
                        chat: typing.Union[str, int, None] = None,
                        user: typing.Union[str, int, None] = None,
                        default: typing.Optional[str] = None) -> typing.Optional[str]:
        chat, user = self.resolve_address(chat=chat, user=user)
        return self.db[chat][user].get("state", self.resolve_state(default))

    async def get_data(self, *,
                       chat: typing.Union[str, int, None] = None,
                       user: typing.Union[str, int, None] = None,
                       default: typing.Optional[str] = None) -> typing.Dict:
        chat, user = self.resolve_address(chat=chat, user=user)
        return copy.deepcopy(self.db[chat][user]['data'])

    async def update_data(self, *,
                          chat: typing.Union[str, int, None] = None,
                          user: typing.Union[str, int, None] = None,
                          data: typing.Dict = None, **kwargs):
        if data is None:
            data = {}
        chat, user = self.resolve_address(chat=chat, user=user)
        with self.get_dict(chat) as chat_dict:
            chat_dict[user]['data'].update(data, **kwargs)

    async def set_state(self, *,
                        chat: typing.Union[str, int, None] = None,
                        user: typing.Union[str, int, None] = None,
                        state: typing.AnyStr = None):
        chat, user = self.resolve_address(chat=chat, user=user)
        with self.get_dict(chat) as chat_dict:
            chat_dict[user]['state'] = self.resolve_state(state)

    async def set_data(self, *,
                       chat: typing.Union[str, int, None] = None,
                       user: typing.Union[str, int, None] = None,
                       data: typing.Dict = None):
        chat, user = self.resolve_address(chat=chat, user=user)
        with self.get_dict(chat) as chat_dict:
            chat_dict[user]['data'] = copy.deepcopy(data)

    async def reset_state(self, *,
                          chat: typing.Union[str, int, None] = None,
                          user: typing.Union[str, int, None] = None,
                          with_data: typing.Optional[bool] = True):
        await self.set_state(chat=chat, user=user, state=None)
        if with_data:
            await self.set_data(chat=chat, user=user, data={})

    def has_bucket(self):
        return True

    async def get_bucket(self, *,
                         chat: typing.Union[str, int, None] = None,
                         user: typing.Union[str, int, None] = None,
                         default: typing.Optional[dict] = None) -> typing.Dict:
        chat, user = self.resolve_address(chat=chat, user=user)
        return copy.deepcopy(self.db[chat][user]['bucket'])

    async def set_bucket(self, *,
                         chat: typing.Union[str, int, None] = None,
                         user: typing.Union[str, int, None] = None,
                         bucket: typing.Dict = None):
        chat, user = self.resolve_address(chat=chat, user=user)
        with self.get_dict(chat) as chat_dict:
            chat_dict[user]['bucket'] = copy.deepcopy(bucket)

    async def update_bucket(self, *,
                            chat: typing.Union[str, int, None] = None,
                            user: typing.Union[str, int, None] = None,
                            bucket: typing.Dict = None, **kwargs):
        if bucket is None:
            bucket = {}
        chat, user = self.resolve_address(chat=chat, user=user)
        with self.get_dict(chat) as chat_dict:
            chat_dict[user]['bucket'].update(bucket, **kwargs)
