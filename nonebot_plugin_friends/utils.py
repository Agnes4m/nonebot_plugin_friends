from nonebot.adapters.onebot.v11 import FriendRequestEvent, GroupRequestEvent

from .config import config


async def friend_add(event: FriendRequestEvent):
    return isinstance(event, FriendRequestEvent)


async def group_friend_add(event: GroupRequestEvent):
    return isinstance(event, GroupRequestEvent) and config.group_request
