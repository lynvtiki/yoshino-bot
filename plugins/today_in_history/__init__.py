import os
import json
import time

from fnbot import ciallo
from fnbot import Message
from fnbot import Send



current_file_path = ciallo.get_current_path(__file__)
path_src = current_file_path + '/src'
path_lssdjt = path_src



@Message.insert_msg()
@ciallo.grace('/today_in_history')
async def _(msg_type:str, num_type:str, rev:'Message'):
    if ciallo.match(rev.msg, ['历史上的今天', '/历史上的今天']):
        now_time = time.strftime("%Y-%m-%d")
        month_now = time.strftime('%m')
        day_now = time.strftime('%d')
        fp = path_lssdjt + f"/{month_now}-{day_now}.json"
        with open(fp, "r", encoding="utf-8") as f:
            day_dict:dict = json.load(f)

        msg_list = [now_time]
        msg_list += [key + ":\n" + value for key,value in day_dict.items()]
        msg:list = ciallo.forward_msg(rev.time, rev.self_id, msg_list)
        Send(rev).send_forward_msg(msg_type, num_type, msg)


