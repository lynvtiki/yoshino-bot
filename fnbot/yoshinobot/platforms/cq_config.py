import os
import sys
import json
from typing import overload

import toml

from ..bot import BotConfig

__all__ = ( "Config",
            "load_config_toml", "load_config_json",

            "load_all_config", "reload_config",
)



def setattr_of_cls(_objcls) -> 'Config':
    if sys.path[0] != '': os.chdir(sys.path[0])
    path_pybot:str = repr(os.getcwd()).replace('\\\\','/')
    path_pybot:str = eval(path_pybot)
    if path_pybot[1] == ":":
        disk_letter,disk_path = path_pybot.split(":",1)
        path_pybot = disk_letter.upper() + ":" + disk_path
    setattr(_objcls, 'path_pybot', path_pybot)
    setattr(_objcls, 'cfginfo', {})
    setattr(_objcls, 'cfgfile', {})
    return _objcls

@setattr_of_cls
class Config(BotConfig):
    """
    Args:
    ```
        self_id: 'Message' | dict | int | str
    ```
    Class Properties:
    ```
        path_pybot: str
        cfginfo: dict{
            'bot_qq':dict,
        }
        cfgfile: dict{
            'toml':['path'],
            'json':['path'],
        }
    ```
    """
    path_pybot: str
    cfginfo: dict
    """
    ```
    dict{
        'bot_qq':dict,
    }
    ```
    """
    cfgfile: dict
    """
    ```
    dict{
        'toml':['path'],
        'json':['path'],
    }
    ```
    """
    __slots__ = (
        'self_id',
        'host', 'port', 'post', 'bot_qq', 'group_list',
        'nickname', 'super_qq', 'admin_list', 'blackqq_list',
    )
    @overload
    def __init__(self, self_id, /): ...

    def __init__(self, self_id = ...):
        super().__init__(self_id)
        self_cfginfo:dict = self.cfginfo.get(self.self_id, {})
        self.host = self_cfginfo.get('host', None)
        self.port = self_cfginfo.get('port', None)
        self.post = self_cfginfo.get('post', None)
        self.bot_qq = self_cfginfo.get('bot_qq', None)
        self.nickname = self_cfginfo.get('nickname', None)
        self.super_qq = self_cfginfo.get('super_qq', None)
        self.admin_list:list = self_cfginfo.get('admin_list', None)
        self.blackqq_list:list = self_cfginfo.get('blackqq_list', None)
        self.group_list:list = self_cfginfo.get('group_list', None)



def _is_legal(_config_info:dict) -> bool:
    if not isinstance(_config_info, dict): return False
    return all((
        'host' in _config_info,
        type(_config_info.get('host')) == str,
        'port' in _config_info,
        type(_config_info.get('port')) == int,
        'post' in _config_info,
        type(_config_info.get('post')) == int,
        'bot_qq' in _config_info,
        type(_config_info.get('bot_qq')) == int,
        'group_list' in _config_info,
        type(_config_info.get('group_list')) == list,
    ))

def _stdize_config_info(_config_info:dict) -> dict:
    host:str = _config_info.get('host', "127.0.0.1")
    port:int = _config_info.get('port', 9900)
    post:int = _config_info.get('post', 9901)
    bot_qq:int = _config_info.get('bot_qq', 0)
    group_list:list = _config_info.get('group_list', [])
    nickname:str = _config_info.get('nickname', "")
    super_qq:int = _config_info.get('super_qq', 0)
    admin_list:list = _config_info.get('admin_list', [])
    blackqq_list:list = _config_info.get('blackqq_list', [])
    return {
        str(bot_qq):{
            'host':host, 'port':port, 'post':post,
            'bot_qq':bot_qq, 'group_list':group_list,
            'nickname':nickname, 'super_qq':super_qq,
            'admin_list':admin_list, 'blackqq_list':blackqq_list,
        }
    }

def _load_config(_config_info:dict):
    config_info:dict = {}
    if _is_legal(_config_info):
        config_info.update(_stdize_config_info(_config_info))
    else:
        for v in _config_info.values():
            if _is_legal(v): config_info.update(_stdize_config_info(v))
    cfginfo = getattr(Config, "cfginfo", {})
    cfginfo.update(config_info)
    setattr(Config, "cfginfo", cfginfo)

def _to_right_path(_path:str) -> str:
    if _path.startswith("./"):
        _path = _path.lstrip("./").rstrip("/")
        _path = Config.path_pybot + '/' + _path
    return _path



def load_config_toml(_path:str):
    """
    Args:
    ```
        _path:str
    ```
    Usages:
    ```
        fnbot.load_config_toml("./pybot.toml")
    ```
    """
    assert ".toml" in _path
    _path = _to_right_path(_path)
    if os.path.isfile(_path):
        cfgfile:dict = getattr(Config, "cfgfile", {})
        config_file_toml:list = cfgfile.get("toml", [])
        config_file_toml.append(_path)
        cfgfile.update({"toml":config_file_toml})
        setattr(Config, "cfgfile", cfgfile)

def load_config_json(_path:str):
    """
    Args:
    ```
        _path:str
    ```
    Usages
    ```
        fnbot.load_config_json("./pybot.json")
    ```
    """
    assert ".json" in _path
    _path = _to_right_path(_path)
    if os.path.isfile(_path):
        cfgfile:dict = getattr(Config, "cfgfile", {})
        config_file_json:list = cfgfile.get("json", [])
        config_file_json.append(_path)
        cfgfile.update({"toml":config_file_json})

def load_all_config():
    cfgfile:dict = getattr(Config, "cfgfile", {})
    config_file_toml:list = cfgfile.get("toml", [])
    config_file_json:list = cfgfile.get("json", [])
    for _ in config_file_toml:
        with open(_, mode='r', encoding="utf-8") as f:
            config_toml:dict = toml.load(f)
        _load_config(config_toml)
    for _ in config_file_json:
        with open(_, mode='r', encoding="utf-8") as f:
            config_json:dict = json.load(f)
        _load_config(config_json)

def reload_config() -> bool:
    if Config.cfginfo == {}: return False
    Config.cfginfo.clear()
    load_all_config()
    return True


