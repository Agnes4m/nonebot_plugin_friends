import json
import time
from typing import List

from nonebot.adapters.onebot.v11 import (
    GROUP_ADMIN,
    GROUP_OWNER,
    Bot,
    FriendRequestEvent,
    GroupMessageEvent,
    GroupRequestEvent,
    Message,
    PrivateMessageEvent,
)
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.plugin import on_command, on_request

from .config import FriendRequest, GroupFriendRequest, config
from .event import pass_group_request, pass_request, save_group_msg, save_msg
from .rule import rule_
from .utils import add_friend, add_group_friend

friend_add = on_request(add_friend, priority=1)
group_friend_add = on_request(add_group_friend, priority=1)


@friend_add.handle()
async def _(
    bot: Bot,
    event: FriendRequestEvent,
):
    logger.info("开始处理好友添加事件")
    # try:
    add_req = json.loads(event.json())
    add_qq: str = str(event.user_id)
    add_comment = event.comment
    add_flag = event.flag
    add_nickname: str = (await bot.get_stranger_info(user_id=event.user_id))["nickname"]
    logger.info(f"已经获取{add_qq}的好友添加事件")

    realtime = time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime(add_req["time"]))
    add_message_id: List[int] = []
    for su_qq in config.master_id:
        logger.info(f"发送给{su_qq}")
        add_message: int = (
            await bot.send_private_msg(
                user_id=int(su_qq),
                message=Message(
                    f"QQ：{add_qq} 请求添加{config.bot_nickname}为好友!\n请求添加时间：{realtime}\n验证信息为：{add_comment}",
                ),
            )
        )["message_id"]
        add_message_id.append(add_message)
    friendrequest = FriendRequest(
        add_id=int(add_qq),
        add_comment=add_comment,
        add_flag=add_flag,
        add_nickname=add_nickname,
        add_message_id=add_message_id,
    )
    await save_msg(friendrequest)


@group_friend_add.handle()
async def _(
    bot: Bot,
    event: GroupRequestEvent,
):
    logger.info("开始处理群聊添加事件")
    # try:
    add_req = json.loads(event.json())
    add_qq: str = str(event.user_id)
    add_group = event.group_id
    add_comment = event.comment
    add_flag = event.flag
    sub_type = event.sub_type
    add_nickname: str = (await bot.get_stranger_info(user_id=event.user_id))["nickname"]
    add_groupname: str = (await bot.get_group_info(group_id=event.group_id))[
        "group_name"
    ]
    logger.info(f"已经获取{add_qq}的群聊申请事件")

    realtime = time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime(add_req["time"]))
    logger.info(f"发送到群聊{add_group}")
    add_message: int = (
        await bot.send_group_msg(
            group_id=int(add_group),
            message=Message(
                f"QQ：{add_qq} 请求请入本群!\n请求添加时间：{realtime}\n验证信息为：{add_comment}",
            ),
        )
    )["message_id"]
    friendrequest = GroupFriendRequest(
        add_id=int(add_qq),
        add_group=add_group,
        add_comment=add_comment,
        add_flag=add_flag,
        add_nickname=add_nickname,
        add_message_id=add_message,
        add_groupname=add_groupname,
        sub_type=sub_type,
    )
    logger.info("来着")
    await save_group_msg(friendrequest, str(add_group))


agree_qq_add = on_command(
    "pass",
    aliases={"允许", "通过", "同意"},
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    priority=2,
    rule=rule_,
)


@agree_qq_add.handle()
async def _(
    bot: Bot,
    event: PrivateMessageEvent,
    matcher: Matcher,
    arg: Message = CommandArg(),
):
    if event.reply:
        add_id = event.reply.message_id
        await pass_request(add_id, bot)
    if not arg:
        await pass_request(None, bot)
    else:
        add_id = arg.extract_plain_text()
        if add_id.isdigit():
            msg = await pass_request(str(add_id), bot)
            await matcher.send(msg)
        else:
            await matcher.finish()

    matcher.stop_propagation()


@agree_qq_add.handle()
async def handle_group_request(
    bot: Bot,
    event: GroupMessageEvent,
    matcher: Matcher,
    arg: Message = CommandArg(),
):
    """处理群聊请求的事件"""
    if event.reply:
        add_id = event.reply.message_id
        await pass_group_request(add_id, str(event.group_id), bot)
    elif arg:
        add_id = arg.extract_plain_text()
        if add_id.isdigit():
            msg = await pass_group_request(add_id, str(event.group_id), bot)
            await matcher.send(msg)
        else:
            await matcher.finish()
    else:
        await matcher.finish()

    matcher.stop_propagation()