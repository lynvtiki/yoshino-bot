import time

from fnbot import ciallo
from fnbot import Message
from fnbot import Send



async def group_sign():
    dev_list = [_ for _ in ciallo(c=None).cfginfo.keys()]
    for _ in dev_list:
        for group_id in ciallo(c=_).group_list:
            Send(_).send_group_sign(group_id)

async def task_start():
    while True:
        h= int(time.strftime("%H"))
        m= int(time.strftime("%M"))
        s= int(time.strftime("%S"))
        awt_time = 86400 -60 - h*3600 - m*60 -s
        if awt_time >= 0:
            time.sleep(awt_time)
        else:
            time.sleep(s + 0.1)
            await group_sign()



@Message.insert()
@ciallo.grace()
async def _():
    await task_start()


