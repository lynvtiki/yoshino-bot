import json
import time
import random
import asyncio
from threading import Lock

from fnbot import ciallo
from fnbot import Message
from fnbot import Send

from .config import path_riddle, path_fable, path_twist



# riddle
def riddle_yield_function(_fp:str):
    with open(_fp, "r", encoding="utf-8") as f:
        _dict:dict = json.load(f)
        _list = list(_dict.keys())
    while True:
        random.shuffle(_list)
        for i in _list: yield (i, _dict[i])

riddle_src_generator = riddle_yield_function(path_riddle)

riddle_lock = Lock()

def riddle_next_function():
    with riddle_lock: return next(riddle_src_generator)


# fable
def fable_yield_function(_fp:str):
    with open(_fp, "r", encoding="utf-8") as f:
        _dict:dict = json.load(f)
        _list = list(_dict.keys())
    while True:
        random.shuffle(_list)
        for i in _list: yield (i, _dict[i])

fable_generator = fable_yield_function(path_fable)

fable_lock = Lock()

def fable_next_function():
    with fable_lock: return next(fable_generator)


# twist
def tist_yield_function(_fp:str):
    with open(_fp, "r", encoding="utf-8") as f:
        _dict:dict = json.load(f)
        _list = list(_dict.keys())
    while True:
        random.shuffle(_list)
        for i in _list: yield (i, _dict[i])

twist_generator = tist_yield_function(path_twist)

twist_lock = Lock()

def twist_next_function():
    with twist_lock: return next(twist_generator)



@Message.insert_msg()
@ciallo.grace('/q and a')
async def _(msg_type:str, num_type:str, rev:'Message'):
    if ciallo.match(rev.msg, ["字谜", "歇后语", "脑筋急转弯",]):
        if rev.msg == "字谜": issue, answer = riddle_next_function()
        elif rev.msg == "歇后语": issue, answer = fable_next_function()
        else: issue, answer = twist_next_function()

        wl = "一二三四五六天"
        weekday = wl[time.localtime().tm_wday]
        now_time = time.strftime("%Y-%m-%d %H:%M:%S")

        msg = (
            f"[CQ:at,qq={str(rev.qq)}]\n"
            f"你有三分钟的时间回答如下问题(共三次机会)\n"
            f"当前时间：\n"
            f"{now_time}\t星期{weekday}"
        )
        msg = ciallo.compat_msg(msg, msg_type, rev)
        Send(rev).send_msg(msg_type, num_type, msg)

        msg = (
            f"[CQ:reply,id={rev.msg_id}]"
            f"[CQ:at,qq={str(rev.qq)}]"
            f"{issue}"
        )
        msg = ciallo.compat_msg(msg, msg_type, rev)
        Send(rev).send_msg(msg_type, num_type, msg)

        @ciallo
        async def schedule(msg_type:str, num_type:str, rev:'Message'):
            while True:
                awtrev:'Message' = await schedule.awt_special_rev()
                schedule.counter += 1
                if all((
                    awtrev.msg == '答案',
                    any((
                        ciallo.is_bot_admin(awtrev),
                        ciallo.is_group_admin(awtrev),
                    )),
                )):
                    schedule.counter -= 1
                    msg = str(answer)
                    Send(rev).send_msg(msg_type, num_type, msg)
                elif awtrev.msg == answer:
                    msg=(
                        f"[CQ:at,qq={str(rev.qq)}]\n"
                        f"恭喜你回答正确！！！"
                    )
                    msg = ciallo.compat_msg(msg, msg_type, rev)
                    Send(rev).send_msg(msg_type, num_type, msg)
                    await schedule.cancel()
                elif schedule.counter >= 3:
                    msg = (
                        f"[CQ:at,qq={str(rev.qq)}]\n"
                        f"回答次数超过上限!!!\n"
                        f"答案是:\n\n"
                        f"{answer}"
                    )
                    msg = ciallo.compat_msg(msg, msg_type, rev)
                    Send(rev).send_msg(msg_type, num_type, msg)
                    await schedule.cancel()
                else:
                    msg=(
                        f"[CQ:at,qq={str(rev.qq)}]\n"
                        f"答案似乎不是这个！！！"
                    )
                    msg = ciallo.compat_msg(msg, msg_type, rev)
                    Send(rev).send_msg(msg_type, num_type, msg)

        @schedule.awtwait
        async def schedule(msg_type:str, num_type:str, rev:'Message'):
            while True:
                awtexcrev = await schedule.awt_exc_rev()
                if all((
                    awtexcrev.msg == '答案',
                    any((
                        ciallo.is_bot_admin(awtexcrev),
                        ciallo.is_group_admin(awtexcrev),
                    )),
                )):
                    msg = answer
                    Send(rev).send_msg(msg_type, num_type, msg)

        @schedule.awtdecline
        async def schedule(msg_type:str, num_type:str, rev:'Message'):
            await asyncio.sleep(180)
            msg = (
                f"[CQ:at,qq={str(rev.qq)}]\n"
                f"等待超时！！！\n"
                f"答案是:\n\n"
                f"{answer}"
            )
            msg = ciallo.compat_msg(msg, msg_type, rev)
            Send(rev).send_msg(msg_type, num_type, msg)
            await schedule.cancel()
        await schedule.start(rev)