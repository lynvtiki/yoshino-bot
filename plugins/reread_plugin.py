import random
import asyncio

from fnbot import ciallo
from fnbot import Message
from fnbot import Send



rev_dict:dict = {}
awt_group:list = []

@Message.insert_group()
@ciallo.grace('/group_fudu')
async def _(msg_type:str, num_type:str, rev:'Message'):
    num_type_msg_list = rev_dict.get(num_type, [])
    num_type_msg_list.append(rev.msg)
    if len(num_type_msg_list) >3: num_type_msg_list.pop(0)
    rev_dict.update({num_type:num_type_msg_list})

    if len(num_type_msg_list) == 3 and all((
        num_type_msg_list[0] == num_type_msg_list[1],
        num_type_msg_list[1] == num_type_msg_list[2],
        num_type not in awt_group, rev.user_id != rev.self_id,
    )): awt_group.append(num_type)
    else: return

    @ciallo
    async def task():
        msg = num_type_msg_list[0]
        Send(rev).send_msg(msg_type, num_type, msg)
        probability = random.uniform(0.88, 88.88)
        while True:
            awtrev = await task.awt_all_rev()
            if any((awtrev.group_id != rev.group_id,
                awtrev.user_id == rev.self_id,)): continue
            if awtrev.msg == msg:
                break_probability = random.uniform(0.88, 100.00)
                if break_probability < probability or probability >= 100:
                    break_msg = "打断施法~"
                    if msg == break_msg: break_msg = "~法施断打"
                    Send(rev).send_msg(msg_type,num_type,break_msg)
                    await task.cancel()
                else:
                    Send(rev).send_msg(msg_type, num_type, msg)
                    probability += random.uniform(0.66, 33.33)
                    if probability >= 100: probability = 100.00
                    await asyncio.sleep(1)
            else:
                await task.cancel()
    await task.start(rev)
    awt_group.remove(num_type)