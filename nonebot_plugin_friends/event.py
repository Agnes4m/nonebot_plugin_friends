from pathlib import Path
from typing import List, Union, Optional
import json

from nonebot.adapters.onebot.v11 import FriendRequestEvent
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot
from .config import Friend_request, config

friend_file = config.frined_paht.joinpath("friend.json")


async def Friend_(event: FriendRequestEvent):
    return isinstance(event, FriendRequestEvent)


async def get_request_data():
    """获取全部好友申请信息"""
    try:
        with open(friend_file, mode="r", encoding="utf-8") as f:
            friend_dict_list: List[dict] = json.load(f)
            friend_requests: List[Friend_request] = [
                Friend_request.parse_obj(friend_dict)
                for friend_dict in friend_dict_list
            ]
    except FileNotFoundError:
        friend_requests: List[Friend_request] = []
    return friend_requests


async def save_request_data(friend_requests: List[Friend_request]):
    """保存好友申请信息"""
    with open(friend_file, mode="w", encoding="utf-8") as f:
        friend_dict_list = [fr.dict() for fr in friend_requests]
        json.dump(friend_dict_list, f, ensure_ascii=False, indent=4)


async def save_msg(msg: Union[Friend_request, int, None], fina: bool = False):
    """好友事件处理
    - Friend_request: 添加待处理的事件
    - int: 解决待处理的qq
    """

    # 加载已保存的好友请求
    friend_requests = await get_request_data()

    # 处理不同类型的消息
    if isinstance(msg, Friend_request):
        logger.info("添加到待处理名单中")
        friend_requests = [fr for fr in friend_requests if fr.add_id != msg.add_id]
        friend_requests.append(msg)

    elif fina:
        logger.info("开始同意最近一次好友请求")
        if friend_requests:
            friend_requests.pop()

    elif isinstance(msg, int):
        logger.info(f"开始同意好友{msg}的好友请求")
        friend_requests = [fr for fr in friend_requests if fr.add_id != msg]

    # 保存更新后的好友请求
    await save_request_data(friend_requests)

    return friend_requests[-1] if friend_requests else None


async def pass_request(add_id: Union[int, str, None], bot: Bot):
    """同意好友事件
    - str:qq号
    - int:信息号
    - None:无"""

    # 加载已保存的好友请求
    friend_requests = await get_request_data()
    if not friend_requests:
        return "暂时没有申请"
    elif not add_id:
        logger.info("开始同意最近一次好友请求")
        last_requests = friend_requests[-1]
        friend_requests.pop()
        return await pass_one([last_requests], last_requests.add_id, bot)
    else:
        logger.info("同意指定好友事件")
        return await pass_one(friend_requests, add_id, bot)


async def pass_one(
    friend_requests: List[Friend_request], add_id: Union[int, str], bot: Bot
):
    """同意好友操作"""
    if isinstance(add_id, int):
        for one_request in friend_requests:
            for one_message_id in one_request.add_message_id:
                if add_id == one_message_id:
                    await bot.set_friend_add_request(
                        flag=one_request.add_flag, approve=True, remark=""
                    )
                    return f"已经同意{one_request.add_nickname}({one_request.add_id})的好友申请"
    else:
        for one_request in friend_requests:
            if add_id == one_request.add_id:
                await bot.set_friend_add_request(
                    flag=one_request.add_flag, approve=True, remark=""
                )
                return f"已经同意{one_request.add_nickname}({one_request.add_id})的好友申请"
    return "没有找到可以同意的申请"
