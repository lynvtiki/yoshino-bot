from typing import overload

import requests

from ..bot import BotSend

from .cq_config import *

__all__ = "Send",



class Send(BotSend):
    """
    Args:
    ```
        self_id: 'Message' | dict | int | str = ...
        host:str = ...
        port:int = ...
    ```
    """
    __slots__ = ('self_id', 'host', 'port',)

    @overload
    def __init__(self, self_id, /): ...
    @overload
    def __init__(self, *, host:str, port:int): ...

    def __init__(self, self_id = ..., host = ..., port = ...):
        super().__init__(self_id)
        if isinstance(self_id, (type(None), type(Ellipsis))):
            assert isinstance(host, str)
            assert isinstance(port, int)
            self.host = host
            self.port = port
        else:
            self.host = Config(self_id).host
            self.port = Config(self_id).port


    def get_status(self) -> dict:
        """get_status

        Returns:
        ```
        {
            "data":{
                "app_enabled":true,
                "app_good":true,
                "app_initialized":true,
                "good":true,
                "online":true,
                "plugins_good":null,
                "stat":{
                    "disconnect_times":0,
                    "last_message_time":0,
                    "lost_times":0,
                    "message_received":0,
                    "message_sent":...,
                    "packet_lost":0,
                    "packet_received":...,
                    "packet_sent":...
                }
            },
            "retcode":0,
            "status":"ok"
        }
        ```
        """
        url = f"http://{self.host}:{self.port}/get_status"
        rps = requests.post(url)
        return rps.json()


    def send_private_msg(self, user_id, message:str, group_id = None):
        """
        Args:
        ```
            user_id:str | int
            message:str
            group_id:str | int | None
        ```
        Returns:
        ```
            msg_id:str | None
        ```
        """
        assert isinstance(user_id, (str, int))
        assert isinstance(message, str)
        url = f"http://{self.host}:{self.port}/send_private_msg"
        if group_id != None:
            assert isinstance(group_id, (str, int))
            data = {
                'user_id':int(user_id),
                'group_id':int(group_id),
                'message':message,
            }
            rps = requests.post(url,data)
            if rps.json()["status"] == "ok":
                msg_id = rps.json()["data"]["message_id"]
            else:
                msg_id = None
            return msg_id
        elif group_id == None:
            data = {
                'user_id':int(user_id),
                'message':message,
            }
            rps = requests.post(url,data)
            if rps.json()["status"] == "ok":
                msg_id = rps.json()["data"]["message_id"]
            else:
                msg_id = None
            return msg_id


    def send_msg(self, msg_type:str, num_type, msg):
        """
        Args:
        ```
            msg_type:str   :('private' or 'group')
            num_type: str | int
            msg: str | int
        ```
        Returns:
        ```
            msg_id:int | None
        ```
        """
        assert isinstance(msg_type, str)
        assert msg_type in ['private', 'group']
        assert isinstance(num_type, (str, int))
        assert isinstance(msg, (str,int))
        url = f"http://{self.host}:{self.port}/send_msg"
        if msg_type == "private":
            data = {
                'message_type':msg_type,
                'user_id':int(num_type),
                'message':msg,
            }
            rps = requests.post(url,data)
            if rps.json()["status"] == "ok":
                msg_id = rps.json()["data"]["message_id"]
            else:
                msg_id = None
            return msg_id
        elif msg_type == "group":
            data = {
                'message_type':msg_type,
                'group_id':int(num_type),
                'message':msg,
            }
            rps = requests.post(url,data)
            if rps.json()["status"] == "ok":
                msg_id = rps.json()["data"]["message_id"]
            else:
                msg_id = None
            return msg_id


    def send_forward_msg(self, msg_type:str, num_type, msg:list):
        """
        Args:
        ```
            msg_type:str   :('private' or 'group')
            num_type:str | int
            msg:list
        ```
        Returns:
        ```
            msg_id:int | None
        """
        assert isinstance(msg_type, str)
        assert msg_type in ['private', 'group']
        assert isinstance(num_type, (str, int))
        assert isinstance(msg, list)
        if msg_type == 'group':
            return self.send_group_forward_msg(num_type, msg)
        else: return self.send_private_forward_msg(num_type, msg)


    def send_private_forward_msg(self, user_id, messages:list):
        """
        Args:
        ```
            user_id:str | int
            messages:list
        ```
        Returns:
        ```
            msg_id:int | None
        ```
        """
        assert isinstance(user_id, (str, int))
        assert isinstance(messages, list)
        data = {
            'user_id':int(user_id),
            'messages':messages,
        }
        url = f"http://{self.host}:{self.port}/send_private_forward_msg"
        rps = requests.post(url,json=data)
        if rps.json()["status"] == "ok":
            msg_id = rps.json()["data"]["message_id"]
        else:
            msg_id = None
        return msg_id


    def send_group_forward_msg(self, group_id, messages:list):
        """
        Args:
        ```
            group_id:str | int
            messages:list
        ```
        Returns:
        ```
            msg_id:int | None
        ```
        """
        assert isinstance(group_id, (str, int))
        assert isinstance(messages, list)
        data = {
            'group_id':int(group_id),
            'messages':messages,
        }
        url = f"http://{self.host}:{self.port}/send_group_forward_msg"
        rps = requests.post(url,json=data)
        if rps.json()["status"] == "ok":
            msg_id = rps.json()["data"]["message_id"]
        else:
            msg_id = None
        return msg_id


    def delete_msg(self, message_id) -> dict:
        """
        Args:
        ```
            message_id:int | str
        ```
        Returns:
        ```
        {
            "data":null,
            "retcode":0,
            "status":"ok"
        }
        or
        {
            "data":null,
            "msg":"MESSAGE_NOT_FOUND",
            "retcode":100,
            "status":"failed",
            "wording":"消息不存在"
        }
        """
        assert isinstance(message_id, (str, int))
        data = {
            'message_id':int(message_id)
        }
        url = f"http://{self.host}:{self.port}/delete_msg"
        rps = requests.post(url,data)
        return rps.json()


    def get_msg(self, message_id) -> dict:
        """
        Args:
        ```
            message_id:str | int
        ```
        Returns:
        ```
        {
            "data":{
                "group":true,
                "group_id":...,
                "message":"...",
                "message_id":...,
                "message_id_v2":"...",
                "message_seq":...,
                "message_type":"group",
                "real_id":...,
                "sender":{
                    "nickname":"...",
                    "user_id":...
                },
                "time":...
            },
            "retcode":0,
            "status":"ok"
        }
        or
        {
            "data":{
                "group":false,
                "message":"...",
                "message_id":...,
                "message_id_v2":"...",
                "message_seq":...,
                "message_type":"private",
                "real_id":...,
                "sender":{
                    "nickname":"...",
                    "user_id":...
                },
                "time":...
            },
            "retcode":0,
            "status":"ok"
        }
        ```
        """
        assert isinstance(message_id, (str, int))
        data = {
            'message_id':int(message_id)
        }
        url = f"http://{self.host}:{self.port}/get_msg"
        rps = requests.post(url,data)
        return rps.json()


    def set_group_kick(self,
        group_id, user_id, reject_add_request:bool = False
    ) -> dict:
        """
        Args:
        ```
            group_id:str | int
            user_id:str | int
            reject_add_request:bool
        ```
        Returns:
        ```
        {
            "data":null,
            "retcode":0,
            "status":"ok"
        }
        ```
        """
        assert isinstance(user_id, (str, int))
        assert isinstance(group_id, (str, int))
        assert isinstance(reject_add_request, bool)
        data = {
            'group_id':int(group_id),
            'user_id':int(user_id),
            'reject_add_request':reject_add_request,
        }
        url = f"http://{self.host}:{self.port}/set_group_kick"
        rps = requests.post(url,json=data)
        return rps.json()


    def set_group_ban(self, group_id, user_id, duration:int = 60) -> dict:
        """
        Args:
        ```
            group_id:str | int
            user_id:str | int
            duration:int
        ```
        Returns:
        ```
        {
            "data":null,
            "retcode":0,
            "status":"ok"
        }
        ```
        """
        assert isinstance(user_id, (str, int))
        assert isinstance(group_id, (str, int))
        assert isinstance(duration, int)
        data = {
            'group_id':int(group_id),
            'user_id':int(user_id),
            'duration':str(duration),
        }
        url = f"http://{self.host}:{self.port}/set_group_ban"
        rps = requests.post(url,data)
        return rps.json()


    def set_group_card(self, group_id, user_id, card:str) -> dict:
        """
        Args:
        ```
            group_id:str | int
            user_id:str | int
            card:str
        ```
        Returns:
        ```
        {
            "data":null,
            "retcode":0,
            "status":"ok"
        }
        ```
        """
        assert isinstance(group_id, (str, int))
        assert isinstance(user_id, (str, int))
        assert isinstance(card, str)
        data = {
            'group_id':int(group_id),
            'user_id':int(user_id),
            'card':card,
        }
        url = f"http://{self.host}:{self.port}/set_group_card"
        rps = requests.post(url,data)
        return rps.json()


    def set_group_leave(self, group_id, is_dismiss:bool = False) -> dict:
        """
        Args:
        ```
            group_id:str | int
            is_dismiss:bool
        ```
        Returns:
        ```
        {
            "data":null,
            "retcode":0,
            "status":"ok"
        }
        ```
        """
        assert isinstance(group_id, (str, int))
        assert isinstance(is_dismiss, bool)
        data = {
            'group_id':int(group_id),
            'is_dismiss':is_dismiss,
        }
        url = f"http://{self.host}:{self.port}/set_group_leave"
        rps = requests.post(url,data)
        return rps.json()


    def get_stranger_info(self, user_id) -> dict:
        """
        Args:
        ```
            user_id:str | int
        ```
        Returns:
        ```
        {
            "data":{
                "age":...,
                "level":...,
                "login_days":...,
                "nickname":"...",
                "qid":"...",
                "sex":"...",
                "user_id":...
            },
            "retcode":0,
            "status":"ok"
        }
        ```
        """
        assert isinstance(user_id, (str, int))
        data = {
            'user_id':int(user_id),
        }
        url = f"http://{self.host}:{self.port}/get_stranger_info"
        rps = requests.post(url,data)
        return rps.json()


    def get_friend_list(self) -> dict:
        """
        Returns:
        ```
        {
            "data":[
                {
                    "nickname":"babyQ",
                    "remark":"babyQ",
                    "user_id":66600000
                },
                ...
            ],
            "retcode":0,
            "status":"ok"
        }
        ```
        """
        url = f"http://{self.host}:{self.port}/get_friend_list"
        rps = requests.post(url)
        return rps.json()


    def delete_friend(self, friend_id) -> dict:
        """?
        Args:
        ```
            friend_id:str | int
        ```
        Returns:
        ```
        {
            "data":null,
            "msg":"FRIEND_NOT_FOUND",
            "retcode":100,
            "status":"failed",
            "wording":"好友不存在"
        }
        ```
        """
        assert isinstance(friend_id, (str, int))
        data = {
            'friend_id':int(friend_id),
        }
        url = f"http://{self.host}:{self.port}/delete_friend"
        rps = requests.post(url,json=data)
        return rps.json()


    def get_group_info(self, group_id) -> dict:
        """
        Args:
        ```
            group_id:str | int
        ```
        Returns:
        ```
        {
            "data":{
                "group_create_time":0,
                "group_id":...,
                "group_level":0,
                "group_name":"...",
                "max_member_count":...,
                "member_count":...
            },
            "retcode":0,
            "status":"ok"
        }
        ```

        Others:
            `https://p.qlogo.cn/gh/{group_id}/{group_id}/100`
        """
        assert isinstance(group_id, (str, int))
        data = {
            'group_id':int(group_id),
        }
        url = f"http://{self.host}:{self.port}/get_group_info"
        rps = requests.post(url,data)
        return rps.json()


    def get_group_list(self) -> dict:
        """
        Returns:
        ```
        {
            "data":[
                {
                    "group_create_time":0,
                    "group_id":...,
                    "group_level":0,
                    "group_name":"...",
                    "max_member_count":200,
                    "member_count":...
                },
                ...
            ],
            "retcode":0,
            "status":"ok"
        }
        ```
        """
        url = f"http://{self.host}:{self.port}/get_group_list"
        rps = requests.post(url)
        return rps.json()


    def get_group_member_info(self, group_id, user_id) -> dict:
        """
        Args:
        ```
            group_id:str | int
            user_id:str | int
        ```
        Returns:
        ```
        {
            "data":{
                "age":0,
                "area":"",
                "card":"",
                "card_changeable":false,
                "group_id":...,
                "join_time":...,
                "last_sent_time":...,
                "level":"...",
                "nickname":"...",
                "role":"...",
                "sex":"...",
                "shut_up_timestamp":0,
                "title":"",
                "title_expire_time":0,
                "unfriendly":false,
                "user_id":...
            },
            "retcode":0,
            "status":"ok"
        }
        ```
        """
        assert isinstance(user_id, (str, int))
        assert isinstance(group_id, (str, int))
        data = {
            'group_id':int(group_id),
            'user_id':int(user_id),
        }
        url = f"http://{self.host}:{self.port}/get_group_member_info"
        rps = requests.post(url,data)
        return rps.json()


    def get_group_member_list(self, group_id) -> dict:
        """
        Args:
        ```
            group_id:str | int
        ```
        Returns:
        ```
        {
            "data":[
                {
                    "age":0,
                    "area":"",
                    "card":"",
                    "card_changeable":false,
                    "group_id":...,
                    "join_time":...,
                    "last_sent_time":...,
                    "level":"...",
                    "nickname":"...",
                    "role":"...",
                    "sex":"...",
                    "shut_up_timestamp":0,
                    "title":"",
                    "title_expire_time":0,
                    "unfriendly":false,
                    "user_id":...
                },...
            ],
            "retcode":0,
            "status":"ok"
        }
        ```
        """
        assert isinstance(group_id, (str, int))
        data = {
            'group_id':int(group_id),
        }
        url = f"http://{self.host}:{self.port}/get_group_member_list"
        rps = requests.post(url,data)
        return rps.json()


    def set_friend_add_request(self,
        flag:str, approve:bool, remark:str = '',
    ) -> dict:
        """
        Args:
        ```
            flag:str
            approve:bool
            remark:str
        ```
        Returns:
        ```
        {'data': None, 'retcode': 0, 'status': 'ok'}
        ```
        """
        assert isinstance(flag, str)
        assert isinstance(approve, bool)
        assert isinstance(remark, str)
        data = {
            'flag':flag,
            'approve':approve,
            'remark':remark,
        }
        url = f"http://{self.host}:{self.port}/set_friend_add_request"
        rps = requests.post(url,json=data)
        return rps.json()


    def set_group_add_request(self,
        flag:str, sub_type:str, approve:bool, reason = None,
    ) -> dict:
        """
        Args:
        ```
            flag:str
            sub_type:str   :('add' or 'invite')
            approve:bool
            reason:str | bool
        ```
        Returns:
        ```
        {'data': None, 'retcode': 0, 'status': 'ok'}
        ```
        """
        assert isinstance(flag, str)
        assert isinstance(sub_type, str)
        assert isinstance(approve, bool)
        assert sub_type in ['add', 'invite']
        data = {
            'flag':flag,
            'sub_type':sub_type,
            'approve':approve,
            'reason':reason,
        }
        url = f"http://{self.host}:{self.port}/set_group_add_request"
        rps = requests.post(url,json=data)
        return rps.json()


    def send_group_sign(self, group_id) -> dict:
        """
        Args:
        ```
            group_id:str | int
        ```
        Returns:
        ```
        {
            "data":null,
            "retcode":0,
            "status":"ok"
        }
        ```
        """
        assert isinstance(group_id, (str, int))
        data = {
            'group_id':int(group_id),
        }
        url = f"http://{self.host}:{self.port}/send_group_sign"
        rps = requests.post(url,data)
        return rps.json()


