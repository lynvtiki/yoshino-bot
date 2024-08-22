import json
import socket
import threading
from typing import overload

from ..bot import BotReceive

from .cq_config import Config

__all__ = ( "Receive",

            "get_rev_msg", "run_receive_server",
)



class Receive(BotReceive):
    """
    Args:
    ```
        self_id: 'Message' | dict | int | str = ...
        host:str = ...
        post:int = ...
    ```
    Class Properties:
    ```
        dev_list: list[self@Receive]
        rev_list: list[dict]
    ```
    """
    dev_list:list = []
    """`list[self@Receive]`"""
    rev_list:list = []
    """`list[dict]`"""
    __slots__ = ('self_id', 'host', 'post',)

    @overload
    def __init__(self, self_id, /): ...
    @overload
    def __init__(self, *, host:str, post:int): ...

    def __init__(self, self_id = ..., host = ..., post = ...):
        super().__init__(self_id)
        self.dev_list.append(self)
        if isinstance(self_id, (type(None), type(Ellipsis))):
            assert isinstance(host, str)
            assert isinstance(post, int)
            self.host = host
            self.post = post
        else:
            self.host = Config(self_id).host
            self.post = Config(self_id).post


    def __call__(self):
        botsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        header = 'HTTP/1.1 200 OK\n\n'
        self._bind(botsocket)
        while True:
            try:
                self._launch(header, botsocket)
            except: ...

    @classmethod
    def _to_json(cls, msg):
        for i in range(len(msg)):
            if msg[i] == "{" and msg[-1] == "\n":
                return json.loads(msg[i:])
        return

    def _bind(self, _botsocket):
        try:
            _botsocket.bind((self.host, self.post))
            _botsocket.listen(100)
        except:
            self._bind(_botsocket)

    def _launch(self, _header, _botsocket):
        conn = _botsocket.accept()[0]
        with conn:
            data = conn.recv(16384).decode(encoding='utf-8')
            conn.sendall((_header).encode(encoding='utf-8'))
            rev_dict = self._to_json(data)
        if rev_dict != None: self.rev_list.append(rev_dict)



def get_rev_msg() -> dict:
    if Receive.rev_list != []: return Receive.rev_list.pop(0)
    else: return {}


def run_receive_server():
    for _ in Config.cfginfo: Receive(_)
    for _ in Receive.dev_list:
        threading.Thread(target=_).start()
