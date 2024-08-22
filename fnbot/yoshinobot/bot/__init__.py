"""
yoshino bot
"""

__all__ = (
    "BotCiallo",
    "BotConfig", "BotReceive", "BotSend",
    "BotInsert", "BotMessage", "BotPlugin",
)



class BotCiallo:
    def __init__(self, self_id = ...):
        """
        Args:
        ```
            self_id: 'BotMessage' | dict | int | str | None
        ```
        """
        assert isinstance(self_id, (
            BotMessage, dict, int, str, type(None), type(Ellipsis),
        ))
        if isinstance(self_id, (str, int)):
            self.self_id = str(self_id)
        elif isinstance(self_id, dict):
            self.self_id = str(self_id.get('self_id', None))
        elif isinstance(self_id, (BotMessage,)):
            self.self_id = str(getattr(self_id, 'self_id', None))
        else:
            self.self_id = None

class BotConfig(BotCiallo):
    def __init__(self, _id = None):
        super(BotConfig, self).__init__(_id)
class BotReceive(BotCiallo):
    def __init__(self, _id = None):
        super(BotReceive, self).__init__(_id)
class BotSend(BotCiallo):
    def __init__(self, _id = None):
        super(BotSend, self).__init__(_id)

class BotInsert(type):
    def __new__(cls, _name:str, _bases:tuple, _dict:dict):
        return type.__new__(cls, _name, _bases, _dict)
    def __init__(self, _name:str, _bases:tuple, _dict:dict):
        return type.__init__(self, _name, _bases, _dict)
class BotMessage:
    def __init__(self):
        super(BotMessage, self).__init__()
class BotPlugin:
    def __init__(self):
        super(BotPlugin, self).__init__()


