

from fnbot import ciallo
from fnbot import Message
from fnbot import Send



@Message.insert_notice()
@ciallo.grace('/upload_group_file')
async def _(msg_type:str, num_type:str, rev:"Message"):
    if rev.notice_type == "group_upload":
        msg = f"[CQ:poke,qq={rev.qq}]"
        Send(rev).send_msg(msg_type, num_type, msg)


@Message.insert_notice()
@ciallo.grace('/group_member_decrease')
async def _(msg_type:str, num_type:str, rev:"Message"):
    if rev.notice_type == "group_decrease" and rev.operator_id == rev.user_id:
        msg = "有个人被···吓跑了！"
        Send(rev).send_msg(msg_type, num_type, msg)


@Message.insert_notice()
@ciallo.grace('/group_member_increase')
async def _(msg_type:str, num_type:str, rev:"Message"):
    if rev.notice_type == "group_increase":
        msg=(
            f"[CQ:at,qq={rev.qq}]\n"
            f"终于等到你了~"
        )
        Send(rev).send_msg(msg_type,num_type,msg)