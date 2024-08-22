import time

from .cq_config import *
from .cq_receive import *
from .cq_send import *

__all__ = ("is_cq_alive",)

__all__ += ( cq_config.__all__ +
             cq_receive.__all__ +
             cq_send.__all__
)



def is_cq_alive() -> bool:
    for _ in list(Config.cfginfo.keys()):
        try:
            result = Send(_).get_status()
            if not 'data' in result and result['data']['online']:
                return is_cq_alive()
        except:
            time.sleep(1)
            return is_cq_alive()
    else:
        return True