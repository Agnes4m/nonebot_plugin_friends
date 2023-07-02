from pathlib import Path
from typing import List,Union,Set
from pydantic import BaseModel, Extra


from nonebot import get_driver

default = get_driver().config.superusers
class Config(BaseModel):
    """基本配置"""
    bot_nickname: str = '宁宁'
    master_nickname: str = '主人'
    master_id: Union[List[str],Set[str],None] = default
    frined_paht:Path = Path('data/friend')
    
    class Config:
        extra = Extra.ignore

class Friend_request(BaseModel):
    """添加用户的信息"""
    add_id: int
    add_comment: str
    add_flag: str
    
    class Config:
        extra = Extra.ignore

config = Config.parse_obj(get_driver().config)

if not config.frined_paht.exists() or not config.frined_paht.is_dir():
    config.frined_paht.mkdir(0o755, parents=True, exist_ok=True)


super_id = config.master_id

