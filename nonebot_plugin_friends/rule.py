from nonebot.adapters.onebot.v11 import MessageEvent, PrivateMessageEvent

from .config import config, default


async def rule_(event: PrivateMessageEvent):
    for one in config.master_id:
        if str(event.user_id) == one:
            return True

    return any(str(event.user_id) == one for one in default)


async def rule_group(event: MessageEvent):
    for one in config.master_id:
        if str(event.user_id) == one:
            return True

    return any(str(event.user_id) == one for one in default)
