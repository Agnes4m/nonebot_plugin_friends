from pathlib import Path
from typing import List,Union
import json

from nonebot.adapters.onebot.v11 import FriendRequestEvent
from nonebot.log import logger

from .config import Friend_request,config
async def Friend_(event: FriendRequestEvent):
    return isinstance(event,FriendRequestEvent)


async def save_msg(msg:Union[Friend_request,int,None],fina:bool = False):
    """好友事件处理
    - Friend_request:添加待处理的事件
    - int:解决待处理的qq
    """
    qq_id = None
    try:
        with open(config.frined_paht.joinpath('friend.json'),mode='r',encoding='utf-8')as f:
            friend_dict_list: List[dict] = json.load(f)
            friend_requests: List[Friend_request] = [Friend_request.parse_obj(friend_dict) for friend_dict in friend_dict_list]

    except FileNotFoundError:
        friend_requests:List[Friend_request] = []
    
    if isinstance(msg,Friend_request):
        logger.info('添加到待处理名单中')
        for one_request in friend_requests:
            if one_request.add_id == msg.add_id:
                friend_requests.remove(one_request)
        friend_requests.append(msg)
        
    elif fina:
        logger.info('开始同意最近一次好友请求')
        latest_friend_request = friend_requests[-1]
        friend_requests.remove(latest_friend_request)
        
    elif isinstance(msg,int):
        logger.info(f'开始同意好友{msg}的好友请求')
        for one_request in friend_requests:
            if one_request.add_id == msg:
                friend_requests.remove(one_request)
    
    with open(config.frined_paht.joinpath('friend.json'),mode='w',encoding='utf-8')as f:
        friend_dict_list = [friend_request.dict() for friend_request in friend_requests]
        json.dump(friend_dict_list, f, ensure_ascii=False, indent=4)
    
    try:
        return latest_friend_request
    except:
        return None