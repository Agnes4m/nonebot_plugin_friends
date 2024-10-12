from nonebot.plugin import PluginMetadata

from .config import ConfigModel
from .matcher import *  # noqa: F403

__version__ = "0.1.4"
__plugin_meta__ = PluginMetadata(
    name="远程同意好友",
    description="自定义远程同意好友和群聊申请",
    usage="被动触发，主动同意",
    type="application",
    config=ConfigModel,
    homepage="https://github.com/Agnes4m/nonebot_plugin_friends",
    supported_adapters={"~onebot.v11"},
    extra={
        "version": __version__,
        "author": "Agnes4m <Z735803792@163.com>",
    },
)
