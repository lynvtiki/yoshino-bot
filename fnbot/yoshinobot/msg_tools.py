import os

from .platforms import Config
from .platforms import Send
from .bot_message import Message



def compat_msg(_msg:str, _msg_type:str, _rev) -> str:
    assert isinstance(_msg, str)
    assert isinstance(_msg_type, str)
    assert isinstance(_rev, (Message, dict))
    assert _msg_type in ['private', 'group']
    if isinstance(_rev, Message): rev_dict:dict = _rev.rev
    if isinstance(_rev, dict): rev_dict:dict = _rev
    if _msg_type == "private":
        if _msg.startswith("[CQ:at,qq="):
            msg = _msg.split("]",1)[-1]
            msg = msg.lstrip("\n")
            msg = "@" + rev_dict['sender']['nickname'] + "\n" + msg
            return msg
        elif _msg.startswith("[CQ:reply,id="):
            _, __, msg = _msg.split("]", 2)
            msg = msg.split("]", 1)[-1]
            msg = "@" + rev_dict['sender']['nickname'] + "\n"+ msg
            msg = _ + "]" + __ + "]" + msg
            return msg
    else:
        return _msg



def forward_msg(name, uin, msg_list:list) -> list:
    assert isinstance(name, (str, int))
    assert isinstance(uin, (str, int))
    assert isinstance(msg_list, list)
    _forward_msg = []
    for msg in msg_list:
        _forward_msg.append({
            "type": "node",
            "data": {
                "name": str(name),
                "uin": str(uin),
                "content": msg
            }
        })
    else:
        return _forward_msg



def is_group_admin(_message:'Message') -> bool:
    assert isinstance(_message, Message)
    self_id = _message.self_id
    group_id = _message.group_id
    user_id = _message.user_id
    if self_id != None and group_id != None and user_id != None:
        role = Send(self_id).get_group_member_info(group_id, user_id)
    else: role = ''
    if 'data' in role: role = role['data']
    if 'role' in role: role = role['role']
    if not isinstance(role, str): role = ''
    return role in ['admin', 'owner']



def is_bot_admin(_message:'Message') -> bool:
    self_id = _message.self_id
    user_id = _message.user_id
    return any((
        self_id == user_id,
        str(user_id) == str(Config(self_id).super_qq),
        user_id in Config(self_id).admin_list,
    ))



def get_current_path(_file:str):
    _path = os.path.realpath(_file)
    _path = _path.rstrip(os.path.basename(_file))
    _path = eval(repr(_path).replace('\\\\','/'))
    _path = str(_path).rstrip('\\\\').rstrip('/')
    return _path