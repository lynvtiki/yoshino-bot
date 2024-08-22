import time
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor

from .bot_insert import get_insert_plugins
from .platforms import Config
from .platforms import load_all_config
from .bot_plugin import load_all_plugin
from .platforms import is_cq_alive
from .platforms import run_receive_server
from .platforms import get_rev_msg
from ._ciallo import schedule

__all__ = "run",



class CoreOfInsert:
    nonparametric_insert_type = ['init', 'insert']
    parametric_insert_type = ['private', 'group', 'notice', 'request']
    __slots__ = ("insert_type", "to_run",)

    def __init__(self, _insert_type:str, _component_list:list):
        self.insert_type = _insert_type
        self.to_run = self.get_to_run(_component_list)
        # to_run:list[function] for parametric_insert_type
        # to_run:dict{'bot_qq':list[function]} for nonparametric_insert_type

    def get_to_run(self, _component_list:list):
        """
        Retuens:
        ```
            to_run:list[function]
            to_run:dict{'bot_qq':list[function]}
        ```
        """
        if self.insert_type in self.nonparametric_insert_type:
            return [_ for _ in _component_list if _.__alive__]
        elif self.insert_type in self.parametric_insert_type:
            to_run_dict:dict = {_:[] for _ in Config.cfginfo.keys()}
            for _ in _component_list:
                if [] == _.__dev__:
                    to_run_dict = {
                        v.append(_) or k:v for k,v in to_run_dict.items()
                    }
                else:
                    for dev in _.__dev__:
                        dev = str(dev)
                        dev_to_list:list = to_run_dict.get(dev, [])
                        dev_to_list.append(_)
                        to_run_dict.update({dev:dev_to_list})
            return to_run_dict

    async def _run_core(self, _rev:dict = {}):
        if self.insert_type in self.nonparametric_insert_type:
            if [] != self.to_run:
                await asyncio.gather(*[_() for _ in self.to_run])
        elif self.insert_type in self.parametric_insert_type:
            to_run_list:list = self.to_run.get(str(_rev.get("self_id")), [])
            to_run_list = [
                _ for _ in to_run_list if (
                    [] == _.__group__ or _rev.get('group_id') in _.__group__
                )
            ]
            to_run_list = sorted(
                to_run_list, key = lambda x:x.__num__, reverse = False
            )
            if [] != to_run_list:
                await asyncio.gather(*[_(_rev) for _ in to_run_list])
    def run(self, _rev:dict = {}): asyncio.run(self._run_core(_rev))



def run_rev_msg():
    # ...
    core_private_list:list = get_insert_plugins("private")
    core_group_list:list = get_insert_plugins("group")
    core_notice_list:list = get_insert_plugins("notice")
    core_request_list:list = get_insert_plugins("request")
    core_private = CoreOfInsert("private", core_private_list)
    core_group = CoreOfInsert("group", core_group_list)
    core_notice = CoreOfInsert("notice", core_notice_list)
    core_request = CoreOfInsert("request", core_request_list)
    # ...

    # it should be execute once as follows:
    core_private.run({'message':None})
    core_group.run({'message':None})
    # main loop: every rev should have a thread belonging to itself
    while True:
        rev = get_rev_msg()
        if {} == rev: time.sleep(0.1); continue
        if all((rev != {}, rev.get('post_type','meta_event') != 'meta_event')):
            schedule.send_rev(rev)
            post_type:str = rev['post_type'] if 'post_type' in rev else ''
            msg_type:str = rev['message_type'] if 'message_type' in rev else ''
            if msg_type == 'private' and all((
                rev.get('user_id') not in Config(rev).blackqq_list,
            )):
                threading.Thread(target=core_private.run, args=(rev,)).start()
            elif msg_type == 'group' and all((
                rev.get('group_id') in Config(rev).group_list,
                rev.get('user_id') not in Config(rev).blackqq_list,
            )):
                threading.Thread(target=core_group.run, args=(rev,)).start()
            elif post_type == 'notice' and all((
                any((
                    rev.get('user_id') not in Config(rev).blackqq_list,
                    rev.get('user_id',None) == None,
                )),
                any((
                    rev.get('group_id') in Config(rev).group_list,
                    rev.get('group_id',None) == None,
                )),
            )):
                threading.Thread(target=core_notice.run, args=(rev,)).start()
            elif post_type == 'request' and all((
                any((
                    rev.get('user_id') not in Config(rev).blackqq_list,
                    rev.get('user_id',None) == None,
                )),
                any((
                    rev.get('group_id') in Config(rev).group_list,
                    rev.get('group_id',None) == None,
                )),
            )):
                threading.Thread(target=core_request.run, args=(rev,)).start()



def _run(_yoshino:str, _max_thread:int):
    assert isinstance(_yoshino, str)
    assert isinstance(_max_thread, int)
    load_all_config()
    load_all_plugin()
    is_cq_alive()
    # ...
    core_init_list:list = get_insert_plugins("init")
    coro_insert_list:list = get_insert_plugins("insert")
    core_init = CoreOfInsert("init", core_init_list)
    coro_insert = CoreOfInsert("insert", coro_insert_list)
    # ...
    core_init.run()
    with ThreadPoolExecutor(max_workers = _max_thread) as executor:
        executor.submit(coro_insert.run)
        executor.submit(run_receive_server)
        executor.submit(run_rev_msg)
        print(_yoshino)
    print("~~~少女祈祷中~~~")


def run(_yoshino:str = "~~~ciallo~~~", _max_thread:int = 3):
    """run yoshino bot
    Args:
    ```
        _yoshino:str = "~~~ciallo~~~"
    ```
    Usages:
    ```
        if "__main__" == __name__:
            fnbot.run()
    ```
    """
    return _run(_yoshino, _max_thread)


