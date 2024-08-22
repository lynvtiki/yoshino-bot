from typing import overload

from .bot import BotMessage

from .bot_insert import *

__all__ = "Message",



class Message(BotMessage):
    """
    Args:
    ```
        _rev:dict = {}
    ```
    """
    __slots__ = (
        "rev",
        "time", "self_id", "post_type",
        "message_type", "notice_type", "request_type",

        "card_new", "card_old", "client", "comment", "duration", "file",
        "flag", "font", "group_id", "honor_type", "message", "message_id",
        "online", "operator_id", "raw_message", "sender_id", "sub_type",
        "target_id", "user_id", "sender",

        "sender_age", "sender_nickname", "sender_sex", "sender_user_id",
        "sender_group_id",
        "sender_area", "sender_card", "sender_level", "sender_role",
        "sender_title",
    )
    @overload
    def __init__(self, _rev:dict, /): ...

    def __init__(self, _rev:dict = {}):
        if None == _rev: _rev = {}
        assert isinstance(_rev, dict)
        self.rev = _rev
        self.time = _rev.get('time', None)
        self.self_id = _rev.get('self_id', None)
        self.post_type = _rev.get('post_type', None)

        self.message_type = _rev.get('message_type', None)
        self.notice_type = _rev.get('notice_type', None)
        self.request_type = _rev.get('request_type', None)

        self.card_new = _rev.get("card_new", None)
        self.card_old = _rev.get("card_old", None)
        self.client = _rev.get("client", None)
        self.comment = _rev.get("comment", None)
        self.duration = _rev.get("duration", None)
        self.file = _rev.get("file", None)
        self.flag = _rev.get("flag", None)
        self.font = _rev.get('font', None)
        self.group_id = _rev.get('group_id', None)
        self.honor_type = _rev.get("honor_type", None)
        self.message = _rev.get('message', None)
        self.message_id = _rev.get('message_id', None)
        self.online = _rev.get("online", None)
        self.operator_id = _rev.get("operator_id", None)
        self.raw_message = _rev.get("raw_message", None)
        self.sender_id = _rev.get("sender_id", None)
        self.sub_type = _rev.get('sub_type', None)
        self.target_id = _rev.get("target_id", None)
        self.user_id = _rev.get('user_id', None)

        self.sender:dict = _rev.get('sender', {})
        # sender (in private or group)
        self.sender_age = self.sender.get('age', None)
        self.sender_nickname = self.sender.get('nickname', None)
        self.sender_sex = self.sender.get('sex', None)
        self.sender_user_id = self.sender.get('user_id', None)
        # sender (only in group)
        self.sender_area = self.sender.get('area', None)
        self.sender_card = self.sender.get('card', None)
        self.sender_level = self.sender.get('level', None)
        self.sender_role = self.sender.get('role', None)
        self.sender_title = self.sender.get('title', None)
        # sender (only in temp)
        self.sender_group_id = self.sender.get('group_id', None)

    @property
    def msg_type(self) -> str:
        if self.group_id != None: return self.message_type
        if self.group_id == None: return 'private'

    @property
    def num_type(self):
        if self.group_id != None: return self.group_id
        if self.group_id == None: return self.user_id

    @property
    def msg(self) -> str:
        if self.message == None: return ''
        else: return self.message
    @msg.setter
    def msg(self, _msg:str):
        assert isinstance(_msg, str)
        self.message = _msg

    @property
    def qq(self): return self.user_id

    @property
    def msg_id(self): return self.message_id



    @overload
    @classmethod
    def insert_init(cls):...
    @overload
    @classmethod
    def insert_init(cls, _dev:list, /):...
    @overload
    @classmethod
    def insert_init(cls, *, _bool:bool):...
    @overload
    @classmethod
    def insert_init(cls,
        _dev:list = [], _group:list = [], _bool:bool = True, _num:int = 0,
    ):...

    @classmethod
    def insert_init(cls,
        _dev:list = [], _group:list = [], _alive:bool = True, _num:int = 0,
    ):
        """
        Args:
        ```
            _dev:list[int | str] = []   :The device number you want to add
            _group:list[int | str] = []   :The group number you want to add
            _alive:bool = True   :Default execution
            _num:int = 0   :the message triggering priority
        ```
        """
        return InsertInit.manage(_dev, _group, _alive, _num)



    @overload
    @classmethod
    def insert(cls):...
    @overload
    @classmethod
    def insert(cls, _dev:list, /):...
    @overload
    @classmethod
    def insert(cls, *, _bool:bool):...
    @overload
    @classmethod
    def insert(cls,
        _dev:list = [], _group:list = [], _bool:bool = True, _num:int = 0,
    ):...

    @classmethod
    def insert(cls,
        _dev:list = [], _group:list = [], _alive:bool = True, _num:int = 0,
    ):
        """
        Args:
        ```
            _dev:list[int | str] = []   :The device number you want to add
            _group:list[int | str] = []   :The group number you want to add
            _alive:bool = True   :Default execution
            _num:int = 0   :the message triggering priority
        ```
        """
        return Insert.manage(_dev, _group, _alive, _num)



    @overload
    @classmethod
    def insert_msg(cls):...
    @overload
    @classmethod
    def insert_msg(cls, _dev:list, /):...
    @overload
    @classmethod
    def insert_msg(cls, *, _bool:bool):...
    @overload
    @classmethod
    def insert_msg(cls,
        _dev:list = [], _group:list = [], _bool:bool = True, _num:int = 0,
    ):...

    @classmethod
    def insert_msg(cls,
        _dev:list = [], _group:list = [], _alive:bool = True, _num:int = 0,
    ):
        """
        Args:
        ```
            _dev:list[int | str] = []   :The device number you want to add
            _group:list[int | str] = []   :The group number you want to add
            _alive:bool = True   :Default execution
            _num:int = 0   :the message triggering priority
        ```
        """
        return InsertMessage.manage(_dev, _group, _alive, _num)



    @overload
    @classmethod
    def insert_private(cls):...
    @overload
    @classmethod
    def insert_private(cls, _dev:list, /):...
    @overload
    @classmethod
    def insert_private(cls, *, _bool:bool):...
    @overload
    @classmethod
    def insert_private(cls,
        _dev:list = [], _group:list = [], _bool:bool = True, _num:int = 0,
    ):...

    @classmethod
    def insert_private(cls,
        _dev:list = [], _group:list = [], _alive:bool = True, _num:int = 0,
    ):
        """
        Args:
        ```
            _dev:list[int | str] = []   :The device number you want to add
            _group:list[int | str] = []   :The group number you want to add
            _alive:bool = True   :Default execution
            _num:int = 0   :the message triggering priority
        ```
        """
        return InsertPrivate.manage(_dev, _group, _alive, _num)



    @overload
    @classmethod
    def insert_group(cls):...
    @overload
    @classmethod
    def insert_group(cls, _dev:list, /):...
    @overload
    @classmethod
    def insert_group(cls, *, _bool:bool):...
    @overload
    @classmethod
    def insert_group(cls,
        _dev:list = [], _group:list = [], _bool:bool = True, _num:int = 0,
    ):...

    @classmethod
    def insert_group(cls,
        _dev:list = [], _group:list = [], _alive:bool = True, _num:int = 0,
    ):
        """
        Args:
        ```
            _dev:list[int | str] = []   :The device number you want to add
            _group:list[int | str] = []   :The group number you want to add
            _alive:bool = True   :Default execution
            _num:int = 0   :the message triggering priority
        ```
        """
        return InsertGroup.manage(_dev, _group, _alive, _num)



    @overload
    @classmethod
    def insert_notice(cls):...
    @overload
    @classmethod
    def insert_notice(cls, _dev:list, /):...
    @overload
    @classmethod
    def insert_notice(cls, *, _bool:bool):...
    @overload
    @classmethod
    def insert_notice(cls,
        _dev:list = [], _notice:list = [], _bool:bool = True, _num:int = 0,
    ):...

    @classmethod
    def insert_notice(cls,
        _dev:list = [], _group:list = [], _alive:bool = True, _num:int = 0,
    ):
        """
        Args:
        ```
            _dev:list[int | str] = []   :The device number you want to add
            _group:list[int | str] = []   :The group number you want to add
            _alive:bool = True   :Default execution
            _num:int = 0   :the message triggering priority
        ```
        """
        return InsertNotice.manage(_dev, _group, _alive, _num)



    @overload
    @classmethod
    def insert_request(cls):...
    @overload
    @classmethod
    def insert_request(cls, _dev:list, /):...
    @overload
    @classmethod
    def insert_request(cls, *, _bool:bool):...
    @overload
    @classmethod
    def insert_request(cls,
        _dev:list = [], _requinsert_request:list = [], _bool:bool = True, _num:int = 0,
    ):...

    @classmethod
    def insert_request(cls,
        _dev:list = [], _group:list = [], _alive:bool = True, _num:int = 0,
    ):
        """
        Args:
        ```
            _dev:list[int | str] = []   :The device number you want to add
            _group:list[int | str] = []   :The group number you want to add
            _alive:bool = True   :Default execution
            _num:int = 0   :the message triggering priority
        ```
        """
        return InsertRequest.manage(_dev, _group, _alive, _num)


