import json
from typing import Dict, List, Union

from nonebot.adapters.onebot.v11 import Bot
from nonebot.log import logger

from .config import (
    FriendRequest,
    FriendRequestEncoder,
    GroupFriendRequest,
    GroupFriendRequestEncoder,
    config,
)

friend_file = config.frined_paht.joinpath("friend.json")
group_file = config.frined_paht.joinpath("group.json")

def create_directories():
    """创建目录"""
    friend_file.parent.mkdir(parents=True, exist_ok=True)
    group_file.parent.mkdir(parents=True, exist_ok=True)

create_directories()


async def get_request_data() -> List[FriendRequest]:
    """获取全部好友申请信息"""
    try:
        with friend_file.open(mode="r", encoding="utf-8") as f:
            friend_dict_list: List[dict] = json.load(f)
            return [FriendRequest.parse_obj(friend_dict) for friend_dict in friend_dict_list]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

async def save_request_data(friend_requests: List[FriendRequest]) -> None:
    """保存好友申请信息"""
    with friend_file.open(mode="w", encoding="utf-8") as f:
        friend_dict_list = [fr.dict() for fr in friend_requests]
        json.dump(
            friend_dict_list,
            f,
            cls=FriendRequestEncoder,
            ensure_ascii=False,
            indent=4,
        )

async def save_msg(msg: FriendRequest) -> None:
    """好友事件添加保存"""
    friend_requests = await get_request_data()
    logger.info("添加到待处理名单中")
    friend_requests = [fr for fr in friend_requests if fr.add_id != msg.add_id] + [msg]
    await save_request_data(friend_requests)

async def pass_request(add_id: Union[int, str, None], bot: Bot) -> str:
    """同意好友事件
    - str: qq号
    - int: 信息号
    - None: 无"""
    friend_requests = await get_request_data()
    
    if not friend_requests:
        return "暂时没有申请"
    
    if add_id is None:
        logger.info("开始同意最近一次好友请求")
        last_request = friend_requests.pop()  # 直接弹出最后一项
        return await pass_one([last_request], last_request.add_id, bot)

    logger.info("同意指定好友事件")
    return await pass_one(friend_requests, add_id, bot)

async def pass_one(friend_requests: List[FriendRequest], add_id: Union[int, str], bot: Bot) -> str:
    """同意好友操作"""
    for one_request in friend_requests:
        if isinstance(add_id, int) and add_id in one_request.add_message_id or isinstance(add_id, str) and add_id == one_request.add_id:
            await approve_request(bot, one_request)
            return f"已经同意{one_request.add_nickname}({one_request.add_id})的好友申请"

    return "没有找到可以同意的申请"

async def approve_request(bot: Bot, request: FriendRequest) -> None:
    """同意好友请求的具体操作"""
    await bot.set_friend_add_request(
        flag=request.add_flag,
        approve=True,
        remark="",
    )


async def get_group_request_data():
    """获取全部群聊申请信息"""
    try:
        with group_file.open(mode="r", encoding="utf-8") as f:
            data: Dict[str, List[Dict[str, Union[str, int]]]] = json.load(f)
            friend_requests: Dict[str, List[GroupFriendRequest]] = {
                key: [GroupFriendRequest(**item) for item in value]  # type: ignore
                for key, value in data.items()
            }
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        friend_requests = {}
    return friend_requests


async def save_group_request_data(friend_requests: Dict[str, List[GroupFriendRequest]]):
    _request = await get_group_request_data()
    _request.update(friend_requests)
    """保存群聊申请信息"""
    with group_file.open(mode="w", encoding="utf-8") as f:
        json.dump(
            _request,
            f,
            cls=GroupFriendRequestEncoder,
            ensure_ascii=False,
            indent=4,
        )


async def save_group_msg(msg: GroupFriendRequest, group_id: str) -> None:
    """群聊事件添加"""
    friend_requests = await get_group_request_data()
    logger.info("添加到待处理名单中")
    friend_requests.setdefault(group_id, [])

    friend_requests[group_id] = [
        fr for fr in friend_requests[group_id] if fr.add_id != msg.add_id
    ] + [msg]
    await save_group_request_data(friend_requests)

async def pass_group_request(add_id: Union[int, str, None], group_id: str, bot: Bot) -> str:
    """同意群聊事件
    - str: qq号
    - int: 信息号
    - None: 无"""
    friend_requests = await get_group_request_data()
    
    # 检查是否有好友请求
    if not friend_requests or group_id not in friend_requests:
        return "暂时没有申请"

    if add_id is None:
        logger.info("开始同意最近一次好友请求")
        last_request = friend_requests[group_id].pop() if friend_requests[group_id] else None
        if last_request:
            return await pass_group([last_request], last_request.add_id, bot)
        return "暂时没有申请"

    logger.info("同意指定好友事件")
    return await pass_group(friend_requests[group_id], add_id, bot)

async def pass_group(friend_requests: List[GroupFriendRequest], add_id: Union[int, str], bot: Bot) -> str:
    """同意群聊操作"""
    for one_request in friend_requests:
        if (isinstance(add_id, int) and add_id == one_request.add_message_id) or \
           (isinstance(add_id, str) and add_id == one_request.add_id):
            await bot.set_group_add_request(
                flag=one_request.add_flag,
                approve=True,
                sub_type=one_request.sub_type,
            )
            friend_requests.remove(one_request)

            # 保存更新后的请求列表
            await save_group_request_data({str(one_request.add_group): friend_requests})
            return f"已经同意{one_request.add_nickname}({one_request.add_id})的好友申请"
    
    return "没有找到可以同意的申请"