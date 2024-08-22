import re
import inspect
import asyncio
from typing import overload

from .platforms import Config
from .platforms import Send
from .platforms import Receive
from .bot_message import Message
from .msg_tools import *

__all__ = "ciallo",

class ciallo:
    """
    Args:
    ```
        _coro:coroutine
        c:'Message' | dict | int | str | None = ...
        r:'Message' | dict | int | str | None = ...
        s:'Message' | dict | int | str | None = ...
        m:dict |None = ...
    ```
    """
    pattern_function_list:list = []
    """`list['function']`"""
    fullargspec_tuple_list:list = []
    """`list[tuple:'FullArgSpec']`"""

    @overload
    def __new__(self, _coro) -> 'schedule': ...
    @overload
    def __new__(self, c) -> 'Config': ...
    @overload
    def __new__(self, r) -> 'Receive': ...
    @overload
    def __new__(self, s) -> 'Send': ...
    @overload
    def __new__(self, m) -> 'Message': ...

    def __new__(self, _coro = ..., c = ..., r = ..., s = ..., m = ...):
        if ... != _coro and schedule._is_legal(_coro):
            new_self_obj = schedule.__new__(schedule, _coro)
            new_self_obj.__init__(_coro)
            return new_self_obj
        elif isinstance(c, (str, int, dict, Message, type(None))):
            if None == c: return Config
            new_self_obj = Config.__new__(Config, c)
            new_self_obj.__init__(c)
            return new_self_obj
        elif isinstance(r, (str, int, dict, Message, type(None))):
            if None == r: return Receive
            new_self_obj = Receive.__new__(Receive, r)
            new_self_obj.__init__(r)
            return new_self_obj
        elif isinstance(s, (str, int, dict, Message, type(None))):
            if None == s: return Send
            new_self_obj = Send.__new__(Send, s)
            new_self_obj.__init__(s)
            return new_self_obj
        elif isinstance(m, (dict, type(None))):
            if None == m: return Message
            new_self_obj = Message.__new__(Message, m)
            new_self_obj.__init__(m)
            return new_self_obj
        return ciallo


    @overload
    @classmethod
    def grace(cls):...
    @overload
    @classmethod
    def grace(cls, _nickname:str, /):...
    @overload
    @classmethod
    def grace(cls, _nickname:str, _cmd:list, /):...

    @classmethod
    def grace(cls, _nickname = None, _cmd = None):
        """
        Args:
        ```
            _nickname: str | None = None
            _cmd: list | None = None
        ```
        """
        assert _nickname == None or isinstance(_nickname, str)
        assert _cmd == None or isinstance(_cmd, list)
        def _decorator(f):
            assert getattr(f.__code__, 'co_argcount', None) in [0, 1, 3]
            assert getattr(f.__code__, 'co_posonlyargcount', None) == 0
            assert getattr(f.__code__, 'co_kwonlyargcount', None) == 0
            if getattr(f.__code__, 'co_argcount', None) == 0:
                async def decorator(): await f()
            elif getattr(f.__code__, 'co_argcount', None) == 1:
                async def decorator(rev:dict): _rev = Message(rev) ; await f(_rev)
            elif getattr(f.__code__, 'co_argcount', None) == 3:
                async def decorator(rev:dict):
                    msg_type:str = 'group' if 'group_id' in rev else 'private'
                    qq:str = str(rev['user_id']) if 'user_id' in rev else ''
                    group_id = str(rev['group_id']) if 'group_id' in rev else ''
                    num_type:str = qq if msg_type == 'private' else group_id
                    _rev = Message(rev)
                    await f(msg_type, num_type, _rev)
            None != _nickname and setattr(decorator, '__nickname__', _nickname)
            None != _cmd and setattr(decorator, '__cmd__', _cmd)
            return decorator
        return _decorator


    @overload
    @classmethod
    def match(cls, _matched:str, _equal:list, /) -> bool:...
    @overload
    @classmethod
    def match(cls, _matched:str, _equal:str, /) -> bool:...
    @overload
    @classmethod
    def match(cls, _matched:str, *, _search:str) -> bool:...
    @overload
    @classmethod
    def match(cls, _matched:str, *, _match:str) -> bool:...
    @overload
    @classmethod
    def match(cls, _matched:str, *, _fullmatch:str) -> bool:...
    @overload
    @classmethod
    def match(cls, _matched:str, _equal = None, /, *,
        _search = None, _match = None, _fullmatch = None,
    ) -> bool:...

    @classmethod
    def match(cls, _matched:str, _equal = None,
        _search = None, _match = None, _fullmatch = None,
    ) -> bool:
        """
        Args:
        ```
            _matched:str
            _equal:str | list | None
            _search:str | None   :(re.search(_search, _matched))
            _match:str | None   :(re.match(_match, _matched))
            _fullmatch:str | None   :(re.fullmatch(_fullmatch, _matched))
        ```
        Returns:
        ```
            bool   :any((
                _equal((_matched == _equal) or (_matched in _equal)),
                re.search(_search, _matched),
                re.match(_match, _matched),
                re.fullmatch(_fullmatch, _matched)
            ))
        ```
        """
        def _(_matched, __equal = _equal,
            __search = _search, __match = _match, __fullmatch = _fullmatch,
        ) -> bool:
            if isinstance(__equal, str): __equal = (_matched == __equal)
            if isinstance(__equal, list): __equal = (_matched in __equal)
            if __search == None: __search = False
            else: __search = re.search(__search, _matched)
            if __match == None: __match = False
            else: __match = re.match(__match, _matched)
            if __fullmatch == None: __fullmatch = False
            else: __fullmatch = re.fullmatch(__fullmatch, _matched)
            return any((__equal, __search, __match, __fullmatch))
        if inspect.getfullargspec(_) not in cls.fullargspec_tuple_list:
            cls.pattern_function_list.append(_)
            cls.fullargspec_tuple_list.append(inspect.getfullargspec(_))
        try: assert isinstance(_matched, (str, int))
        except AssertionError: return False

        assert _equal == None or isinstance(_equal, (str, list))
        assert _search == None or isinstance(_search, str)
        assert _match == None or isinstance(_match, str)
        assert _fullmatch == None or isinstance(_fullmatch, str)
        if isinstance(_equal, str): _equal = (_matched == _equal)
        if isinstance(_equal, list): _equal = (_matched in _equal)
        if _search == None: _search = False
        else: _search = re.search(_search, _matched)
        if _match == None: _match = False
        else: _match = re.match(_match, _matched)
        if _fullmatch == None: _fullmatch = False
        else: _fullmatch = re.fullmatch(_fullmatch, _matched)
        return any((_equal, _search, _match, _fullmatch))


    @classmethod
    def compat_msg(cls, _msg:str, _msg_type:str, _rev) -> str:
        """
        Make the messages to be sent compatible with
        group chats and private chats

        Args:
        ```
            _msg:str
            _msg_type:str
            _rev: dict | 'Message'
        ```
        """
        return compat_msg(_msg, _msg_type, _rev)


    @overload
    @classmethod
    def forward_msg(cls, name:str, uin:int, msg_list:list, /) -> list:...
    @overload
    @classmethod
    def forward_msg(cls, name:int, uin:str, msg_list:list, /) -> list:...
    @overload
    @classmethod
    def forward_msg(cls, name:str, uin:str, msg_list:list, /) -> list:...
    @overload
    @classmethod
    def forward_msg(cls, name:int, uin:int, msg_list:list, /) -> list:...

    @classmethod
    def forward_msg(cls, name, uin, msg_list:list) -> list:
        """
        Args:
        ```
            name:str | int
            uin:str | int
            msg_list:list[str]
        ```
        """
        return forward_msg(name, uin, msg_list)


    @classmethod
    def is_group_admin(cls, _message:'Message') -> bool:
        return is_group_admin(_message)


    @classmethod
    def is_bot_admin(cls, _message:'Message') -> bool:
        return is_bot_admin(_message)


    @classmethod
    def get_current_path(cls, _file:str):
        """`_file` should be `__file__`"""
        return get_current_path(_file)



class schedule:
    scheduled_list:list = []
    __slots__ = (
        "__awtstart__", "__awtwait__", "__awtdecline__", "__death__",
        "timer", "counter",
        "all_rev_list", "special_rev_list", "exc_rev_list",
        "former_rev",
        "self_id", "msg_type", "num_type", "user_id", "group_id", "msg_id",
    )
    def __init__(self, _awtstart = ..., _awtwait = ..., _awtdecline = ...):
        self.timer = 666
        self.counter = 0
        self.all_rev_list = []
        self.special_rev_list = []
        self.exc_rev_list = []
        self.__death__ = self.__death_timer__
        self.__awtwait__ = self.__forever__
        self.__awtdecline__ = self.__forever__
        if _awtstart != ...: self.__awtstart__ = _awtstart
        if _awtwait != ...: self.__awtwait__ = _awtwait
        if _awtdecline != ...: self.__awtdecline__ = _awtdecline
    async def __forever__(): True and ... or False ; lambda:... ; return ; raise
    __forever__ = staticmethod(__forever__)
    async def __death_timer__(self): await asyncio.sleep(self.timer) ; raise RuntimeError
    async def __run__(self):
        self.scheduled_list.append(self)
        if 0 == getattr(self.__awtstart__.__code__, 'co_argcount', None):
            task_tuple = (asyncio.create_task(self.__awtstart__()), )
        elif 1 == getattr(self.__awtstart__.__code__, 'co_argcount', None):
            task_tuple = (asyncio.create_task(self.__awtstart__(self.former_rev)), )
        else:
            task_tuple = (
                asyncio.create_task(self.__awtstart__(
                    self.msg_type, self.num_type, self.former_rev
                )),
            )
        if 0 == getattr(self.__awtwait__.__code__, 'co_argcount', None):
            task_tuple += (asyncio.create_task(self.__awtwait__()), )
        elif 1 == getattr(self.__awtwait__.__code__, 'co_argcount', None):
            task_tuple += (asyncio.create_task(self.__awtwait__(self.former_rev)), )
        else:
            task_tuple += (
                asyncio.create_task(self.__awtwait__(
                    self.msg_type, self.num_type, self.former_rev
                )),
            )
        if 0 == getattr(self.__awtdecline__.__code__, 'co_argcount', None):
            task_tuple += (asyncio.create_task(self.__awtdecline__()), )
        elif 1 == getattr(self.__awtdecline__.__code__, 'co_argcount', None):
            task_tuple += (asyncio.create_task(self.__awtdecline__(self.former_rev)), )
        else:
            task_tuple += (
                asyncio.create_task(self.__awtdecline__(
                    self.msg_type, self.num_type, self.former_rev
                )),
            )
        task_tuple += (asyncio.create_task(self.__death__()), )
        try: await asyncio.wait(task_tuple, return_when = 'FIRST_EXCEPTION')
        finally:
            if self in self.scheduled_list: self.scheduled_list.remove(self)
            del self
    @classmethod
    def _is_legal(cls, _coro = ...) -> bool:
        return all((
            getattr(_coro.__code__, "co_flags", None) in [147, 195],
            getattr(_coro.__code__, 'co_argcount', None) in [0, 1, 3],
            getattr(_coro.__code__, 'co_posonlyargcount', None) == 0,
            getattr(_coro.__code__, 'co_kwonlyargcount', None) == 0,
        ))
    def awtstart(self, _coro = ...) -> 'schedule':
        assert self._is_legal(_coro) ; self.__awtstart__ = _coro ; return self
    def awtwait(self, _coro = ...) -> 'schedule':
        assert self._is_legal(_coro) ; self.__awtwait__ = _coro ; return self
    def awtdecline(self, _coro = ...) -> 'schedule':
        assert self._is_legal(_coro) ; self.__awtdecline__ = _coro ; return self
    async def start(self, _former_rev:'Message' = Message({})):
        self.former_rev = _former_rev
        self.self_id = _former_rev.self_id
        self.msg_type = _former_rev.msg_type
        self.num_type = _former_rev.num_type
        self.user_id = _former_rev.user_id
        self.group_id = _former_rev.group_id
        self.msg_id = _former_rev.msg_id
        await self.__run__()
    async def cancel(self): raise RuntimeError
    async def forever(self): self.__death__ = self.__forever__


    @classmethod
    def send_rev(cls, _rev:dict):
        rev = Message(_rev)
        _bool_list:list = [_(rev.msg) for _ in ciallo.pattern_function_list]
        if cls.scheduled_list != []:
            _:'schedule'
            for _ in cls.scheduled_list:
                if _bool_list.count(False) == len(_bool_list):
                    if all((
                        None != rev.msg, _.self_id == rev.self_id,
                        _.user_id == rev.user_id, _.group_id == rev.group_id,
                    )):
                        _.special_rev_list.append(rev)
                    elif all((
                        None != rev.msg, _.self_id == rev.self_id,
                        _.user_id != rev.user_id, _.group_id == rev.group_id,
                    )):
                        _.exc_rev_list.append(rev)
                    if all((
                        None != rev.msg, _.self_id == rev.self_id,
                    )):
                        _.all_rev_list.append(rev)

    async def awt_all_rev(self) -> 'Message':
        while True:
            if self.all_rev_list != []:
                return self.all_rev_list.pop(0)
            await asyncio.sleep(0.1)

    async def awt_special_rev(self) -> 'Message':
        while True:
            if self.special_rev_list != []:
                return self.special_rev_list.pop(0)
            await asyncio.sleep(0.1)

    async def awt_exc_rev(self) -> 'Message':
        while True:
            if self.exc_rev_list != []:
                return self.exc_rev_list.pop(0)
            await asyncio.sleep(0.1)


