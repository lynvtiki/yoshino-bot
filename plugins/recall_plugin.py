import asyncio

from fnbot import ciallo
from fnbot import Message
from fnbot import Send



@Message.insert_notice()
@ciallo.grace('/group_recall')
async def _(msg_type:str, num_type:str, rev:'Message'):
    if rev.notice_type == "group_recall" and all((
        rev.operator_id != rev.self_id, rev.user_id != rev.self_id,
    )):
        recall_rev = Send(rev).get_msg(rev.msg_id)['data']
        recall_rev = Message(recall_rev)
        recall_msg = recall_rev.msg

        msg = f"[CQ:poke,qq={recall_rev.sender_user_id}]"
        Send(rev).send_msg(msg_type, num_type, msg)

        msg = recall_msg
        msg_id = Send(rev).send_msg(msg_type, num_type, msg)

        @ciallo
        async def task():
            await asyncio.sleep(3)
            Send(rev).delete_msg(msg_id)
            await task.cancel()
        await task.start(rev)


@Message.insert_notice()
@ciallo.grace('/private_recall')
async def _(rev:"Message"):
    if rev.notice_type == "friend_recall":
        recall_rev = Send(rev).get_msg(rev.msg_id)['data']
        recall_rev = Message(recall_rev)
        _qq = recall_rev.sender_user_id
        msg = f"{_qq}\t\t\t的消息在私聊中被撤回了:\n\n{recall_rev.msg}"
        Send(rev).send_msg("private",ciallo(c=rev).super_qq,msg)