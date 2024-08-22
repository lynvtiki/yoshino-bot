

from fnbot import ciallo
from fnbot import Message
from fnbot import Send



@Message.insert_request()
@ciallo.grace('/add_friend')
async def _(rev:"Message"):
    if rev.request_type == "friend":
        Send(rev).set_friend_add_request(rev.flag, True)
