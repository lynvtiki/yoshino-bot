from typing import overload

from .bot import BotInsert

__all__ = ( "Insert",
            "InsertInit", "InsertMessage",
            "InsertPrivate", "InsertGroup",
            "InsertNotice", "InsertRequest",

            "get_insert_plugins"
)



def _is_legal_decorated(f) -> bool:
    return all((
        getattr(f.__code__, 'co_flags', 0) in [147, 195],
    ))

def _update_manage_component(_insert_type:str, _f):
    f_list:list = Insert.manage_component_dict.get(_insert_type, [])
    f_list.append(_f)
    Insert.manage_component_dict.update({_insert_type:f_list})

class Insert(BotInsert):
    """
    Class Properties:
    ```
        insert_type:str = "insert"
        manage_component_dict: dict{
            'insert_type': list[function],
        }
    ```
    """
    insert_type:str = "insert"
    manage_component_dict:dict = {}
    """
    ```
        dict{
            'insert_type': list[function],
        }
    ```
    """
    def __new__(cls, _name:str, _bases:tuple, _dict:dict):
        return type.__new__(cls, _name, _bases, _dict)

    def __init__(self, _name:str, _bases:tuple, _dict:dict):
        if _name in ['InsertInit']: self.insert_type = 'init'
        elif _name in ['InsertMessage']: self.insert_type = 'message'
        elif _name in ['InsertPrivate']: self.insert_type = 'private'
        elif _name in ['InsertGroup']: self.insert_type = 'group'
        elif _name in ['InsertNotice']: self.insert_type = 'notice'
        elif _name in ['InsertRequest']: self.insert_type = 'request'
        return type.__init__(self, _name, _bases, _dict)


    @overload
    @classmethod
    def manage(cls): ...
    @overload
    @classmethod
    def manage(cls, _dev:list, /): ...
    @overload
    @classmethod
    def manage(cls, *, _bool:bool): ...
    @overload
    @classmethod
    def manage(cls,
        _dev:list = [], _group:list = [], _bool:bool = True, _num:int = 0,
    ): ...

    @classmethod
    def manage(cls,
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
        def decorator(f):
            assert _is_legal_decorated(f)
            assert isinstance(_dev, list)
            assert isinstance(_group, list)
            assert isinstance(_alive, bool)
            assert isinstance(_num, int)
            setattr(f, "__dev__", _dev)
            setattr(f, "__group__", _group)
            setattr(f, "__alive__", _alive)
            setattr(f, "__num__", _num)
            if cls.insert_type == "message":
                _update_manage_component("private", f)
                _update_manage_component("group", f)
                return f
            _update_manage_component(cls.insert_type, f)
            return f
        return decorator



class InsertInit(Insert, metaclass = Insert):
    def __new__(cls): pass
class InsertMessage(Insert, metaclass = Insert):
    def __new__(cls): pass
class InsertPrivate(Insert, metaclass = Insert):
    def __new__(cls): pass
class InsertGroup(Insert, metaclass = Insert):
    def __new__(cls): pass
class InsertNotice(Insert, metaclass = Insert):
    def __new__(cls): pass
class InsertRequest(Insert, metaclass = Insert):
    def __new__(cls): pass



def get_insert_plugins(_insert_type:str) -> list:
    return Insert.manage_component_dict.get(_insert_type, [])