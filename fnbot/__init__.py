r"""This module is for quick import

For the convenience of use,this module imports some content from sub-modules,
the following content can be imported directly through this module
"""
from .yoshinobot import run as run
from .yoshinobot import load_config_toml as load_config_toml
from .yoshinobot import load_config_json as load_config_json
from .yoshinobot import insert_plugin as insert_plugin
from .yoshinobot import insert_plugins_dir as insert_plugins_dir
from .yoshinobot import insert_the_plugin as insert_the_plugin

from .yoshinobot import ciallo as ciallo
from .yoshinobot import Config as Config
from .yoshinobot import Receive as Receive
from .yoshinobot import Send as Send
from .yoshinobot import Message as Message

from .yoshinobot import YOSHINO as YOSHINO

from .__version__ import (
    __title__,
    __version__,
    __description__,
    __url__,
    __author__,
    __author_email__,
)

CIALLO = "CIALLO"