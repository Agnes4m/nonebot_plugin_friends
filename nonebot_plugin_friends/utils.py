from nonebot.adapters.onebot.v11 import FriendRequestEvent, GroupRequestEvent

from .config import config


async def add_friend(event: FriendRequestEvent):
    return isinstance(event, FriendRequestEvent)


async def add_group_friend(event: GroupRequestEvent):
    return isinstance(event, GroupRequestEvent) and config.group_request
