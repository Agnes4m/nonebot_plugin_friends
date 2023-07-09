from nonebot.adapters.onebot.v11 import (
    MessageEvent,
    FriendRequestEvent,
    GroupRequestEvent,
    PrivateMessageEvent,
)
from .config import config, default


async def rule_(event: PrivateMessageEvent):
    for one in config.master_id:
        if str(event.user_id) == one:
            return True

    for one in default:
        if str(event.user_id) == one:
            return True
    return False


async def rule_group(event: MessageEvent):
    for one in config.master_id:
        if str(event.user_id) == one:
            return True

    for one in default:
        if str(event.user_id) == one:
            return True
    return False


async def Friend_(event: FriendRequestEvent):
    return isinstance(event, FriendRequestEvent)


async def Group_Friend(event: GroupRequestEvent):
    return isinstance(event, GroupRequestEvent) and config.group_request
