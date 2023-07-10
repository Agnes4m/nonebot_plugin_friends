from pathlib import Path
from typing import List, Union, Optional, Dict
import json

from nonebot.adapters.onebot.v11 import FriendRequestEvent
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot
from .config import *

friend_file = config.frined_paht.joinpath("friend.json")
group_file = config.frined_paht.joinpath("group.json")


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
        json.dump(
            friend_dict_list, f, cls=FriendRequestEncoder, ensure_ascii=False, indent=4
        )


async def save_msg(msg: Friend_request):
    """好友事件添加保存"""

    # 加载已保存的好友请求
    friend_requests = await get_request_data()

    # 处理不同类型的消息
    logger.info("添加到待处理名单中")
    friend_requests = [fr for fr in friend_requests if fr.add_id != msg.add_id]
    friend_requests.append(msg)

    # 保存更新后的好友请求
    await save_request_data(friend_requests)


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


async def get_group_request_data():
    """获取全部群聊申请信息"""
    try:
        with open(group_file, mode="r", encoding="utf-8") as f:
            data: Dict[str, List[Dict[str, Union[str, int]]]] = json.load(f)
            friend_requests: Dict[str, List[Group_Friend_request]] = {
                key: [Group_Friend_request(**item) for item in value]  # type: ignore
                for key, value in data.items()
            }
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        friend_requests: Dict[str, List[Group_Friend_request]] = {}
    return friend_requests


async def save_group_request_data(
    friend_requests: Dict[str, List[Group_Friend_request]]
):
    _request = await get_group_request_data()
    _request.update(friend_requests)
    """保存群聊申请信息"""
    with open(group_file, mode="w", encoding="utf-8") as f:
        json.dump(
            _request,
            f,
            cls=GroupFriendRequestEncoder,
            ensure_ascii=False,
            indent=4,
        )


async def save_group_msg(msg: Group_Friend_request, group_id: str):
    """群聊事件添加"""

    # 加载已保存的好友请求
    friend_requests = await get_group_request_data()

    # 处理不同类型的消息
    logger.info("添加到待处理名单中")

    if group_id not in friend_requests:
        friend_requests[group_id] = []

    friend_requests[group_id] = [
        fr for fr in friend_requests[group_id] if fr.add_id != msg.add_id
    ]
    friend_requests[group_id].append(msg)

    # 保存更新后的好友请求
    await save_group_request_data(friend_requests)


async def pass_group_request(add_id: Union[int, str, None], group_id: str, bot: Bot):
    """同意群聊事件
    - str: qq号
    - int: 信息号
    - None: 无"""

    # 加载已保存的好友请求
    friend_requests = await get_group_request_data()
    if not friend_requests:
        return "暂时没有申请"
    elif add_id is None:
        logger.info("开始同意最近一次好友请求")
        if group_id in friend_requests and friend_requests[group_id]:
            last_requests = friend_requests[group_id][-1]
            friend_requests[group_id].pop()
            return await pass_group([last_requests], last_requests.add_id, bot)
        else:
            return "暂时没有申请"
    else:
        logger.info("同意指定好友事件")
        if group_id in friend_requests and friend_requests[group_id]:
            return await pass_group(friend_requests[group_id], add_id, bot)
        else:
            return "暂时没有申请"


async def pass_group(
    friend_requests: List[Group_Friend_request],
    add_id: Union[int, str],
    bot: Bot,
):
    """同意群聊操作"""
    if isinstance(add_id, int):
        for one_request in friend_requests:
            print(one_request, type(one_request))
            if add_id == one_request.add_message_id:
                await bot.set_group_add_request(
                    flag=one_request.add_flag,
                    approve=True,
                    sub_type=one_request.sub_type,
                )
                for one in friend_requests:
                    if int(one.add_id) == add_id:
                        friend_requests.remove(one)

                await save_group_request_data(
                    {str(one_request.add_group): friend_requests}
                )
                return f"已经同意{one_request.add_nickname}({one_request.add_id})的好友申请"
    else:
        for one_request in friend_requests:
            if add_id == one_request.add_id:
                await bot.set_group_add_request(
                    flag=one_request.add_flag,
                    approve=True,
                    sub_type=one_request.sub_type,
                )
                for one in friend_requests:
                    if str(one.add_id) == add_id:
                        friend_requests.remove(one)

                await save_group_request_data(
                    {str(one_request.add_group): friend_requests}
                )
                return f"已经同意{one_request.add_nickname}({one_request.add_id})的好友申请"
    return "没有找到可以同意的申请"
