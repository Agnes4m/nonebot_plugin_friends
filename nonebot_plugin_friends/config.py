import json
from pathlib import Path
from typing import List, Optional, Set, Union

from nonebot import get_driver, get_plugin_config
from pydantic import BaseModel, Extra

default = get_driver().config.superusers


class ConfigModel(BaseModel):
    """基本配置"""

    bot_nickname: str = "宁宁"
    master_nickname: str = "主人"
    master_id: Union[List[str], Set[str]] = default
    frined_paht: Path = Path("data/friend")
    group_request: bool = True

    class Config:
        extra = Extra.ignore


class FriendRequest(BaseModel):
    """添加用户的信息"""

    add_id: int
    add_comment: Optional[str]
    add_flag: str
    add_nickname: str
    add_message_id: List[int]

    class Config:
        extra = Extra.ignore


class GroupFriendRequest(BaseModel):
    """群聊申请用户的信息"""

    add_id: int
    add_group: int
    add_comment: Optional[str]
    add_flag: str
    add_nickname: str
    add_message_id: int
    add_groupname: str
    sub_type: str

    class Config:
        extra = Extra.ignore


class FriendRequestEncoder(json.JSONEncoder):
    def _default(self, obj):
        if isinstance(obj, FriendRequest):
            return obj.dict()
        return super().default(obj)


class GroupFriendRequestEncoder(json.JSONEncoder):
    def _default(self, obj):
        if isinstance(obj, GroupFriendRequest):
            return obj.dict()
        return super().default(obj)


config = get_plugin_config(ConfigModel)
