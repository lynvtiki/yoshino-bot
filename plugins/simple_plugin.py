import time

from fnbot import ciallo
from fnbot import Message
from fnbot import Send



@Message.insert_msg()
@ciallo.grace('/help')
async def _(msg_type:str, num_type:str, rev:'Message'):
    if ciallo.match(rev.msg, ["菜单", "帮助", "基本功能"]):
        msg = "暂时没有~"
        Send(rev).send_msg(msg_type, num_type, msg)


@Message.insert_msg()
@ciallo.grace('/time')
async def _(msg_type:str, num_type:str, rev:'Message'):
    if ciallo.match(rev.msg, ['时间', '/时间']):
        wl = "一二三四五六天"
        weekday = wl[time.localtime().tm_wday]
        now_time = time.strftime("%Y-%m-%d %H:%M:%S")
        msg = f"{now_time}\t星期{weekday}"
        Send(rev).send_msg(msg_type, num_type, msg)