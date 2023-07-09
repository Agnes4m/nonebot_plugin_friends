import time
import json


from nonebot.adapters.onebot.v11 import (
    Bot,
    FriendRequestEvent,
    MessageEvent,
    Message,
    PrivateMessageEvent,
)
from nonebot.permission import SUPERUSER
from nonebot.matcher import Matcher
from nonebot.plugin import on_command, on_request
from nonebot.params import CommandArg
from nonebot.log import logger
from nonebot.plugin import PluginMetadata


from .config import *
from .utils import *
from .event import *


__version__ = "0.0.1"
__plugin_meta__ = PluginMetadata(
    name="远程同意好友",
    description="自定义远程同意好友",
    usage="被动触发，主动同意",
    type="application",
    homepage="https://github.com/Agnes4m/nonebot_plugin_friends",
    supported_adapters={"~onebot.v11"},
    extra={
        "version": __version__,
        "author": "Agnes4m <Z735803792@163.com>",
    },
)


add_friend = on_request(Friend_, priority=1, block=True)


async def rule_(event: MessageEvent):
    for one in config.master_id:
        if str(event.user_id) == one:
            return True

    for one in default:
        if str(event.user_id) == one:
            return True
    return False


agree_qq_add = on_command("pass", aliases={"允许", "通过", "同意"}, rule=rule_)


@add_friend.handle()
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
                    f"QQ：{add_qq} 请求添加{config.bot_nickname}为好友!\n请求添加时间：{realtime}\n验证信息为：{add_comment}"
                ),
            )
        )["message"]
        add_message_id.append(add_message)
    friend_request = Friend_request(
        add_id=int(add_qq),
        add_comment=add_comment,
        add_flag=add_flag,
        add_nickname=add_nickname,
        add_message_id=add_message_id,
    )
    await save_msg(friend_request)


@agree_qq_add.handle()
async def _(
    bot: Bot, event: MessageEvent, matcher: Matcher, arg: Message = CommandArg()
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
