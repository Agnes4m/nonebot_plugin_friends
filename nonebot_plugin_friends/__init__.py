import time
import json


from nonebot.adapters.onebot.v11 import (
    Bot, 
    FriendRequestEvent,
    MessageEvent, 
    Message,
    PrivateMessageEvent
    )
from nonebot.permission import SUPERUSER
from nonebot.matcher import Matcher
from nonebot.plugin import on_command, on_request
from nonebot.params import CommandArg
from nonebot.log import logger
from nonebot.plugin import PluginMetadata


from .config import *
from .utils import *

logo ="""
    ......                  ` .]]@@@@@@@@@@@@@@@@@@@@@@@@@@@@@OO^       
    ......                ,/@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@OO^       
    ......            /O@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@OO^       
    `.....           ,@^=.OOO\/\@@@@@@@@@@@@@@@@@@@@OO//@@@@@/OO\]]]OO\]
    ``....          ,@@/=^OOOOOOOO@@@@@@@@@@@\]OOOOOOO^^=@@@@OOOOOOOOOOO
    `.....          O@O^==OOOOOOOO@@@/.,@@@OOOOOOOOOOO\O,@@@@OOOOOOOOO@@
    ......    ,    .@@@^=`OOOOOOOOO/  ,O@@OOOOOOOOOOOOOO.O@@@OO/[[[[[[[.
    ......    =..,//@@@^=`OOOOOOOOO@.*=@@@OOOOOOOOOOOOOO]@@@OOO.     ,/`
    ......    =.\O]`,@O^\=OOOO@@@@@@O`=@@@@@@@OOOOOOOO*O,OO^....[[``]./]
    ......    ,^.oOoO@O^=,OO@@@@@OoO`\O\OO@@@@OOOOOOOOO]@@^.]]]/OOOo.,OO
    ......     =.=OOOO@@@@/[[=/.^,/....*.=^,[O@@@@OOOO.@@OOOOOOOOO/..OOO
    ......      \.\OO`.,....*`.=.^.......=....=@O[\@@O@@[^ ,`.=Oo*.,OOO/
    ......       ,@,`...  ....=^/......../....=/O^....\..O]/[\O[*]/OOO. 
    ......       ]@^.,....*..=O\^........^..*.O.\O.^..=^\..,\/\@OOO[.   
    ......    ,,`O^.,..../.,O`//........=..=`=^.=O`O..=^..OOO*/OOO.     
    ......   .=.=@..^...=^/O`*OO.]...o**\.,/=^...O^@^..^...OO^=`OOO`    
    ......  `=.,O^./.*.,OO`,.,/@/.*,O`,O*/@/`....\O\^......Oo^.^,OOO.   
    ...... .,`.o=^=^.../`...]/`***/O^/@oO@`..[[[[\/=\......O^^...=OO^   
    ......  ^.=`O^O.*.=\],]]]/\O/\@O[=O/`        =.=O....=^O^*....OOO.  
    ...... =../=OO^.*.=@@[[,@@@\ .. ..    ,\@@@@@] =O...`=^@`.....=OO^  
    ...... `..^=OO^.^,@`  ^ =oO\          .O\O@\.,\@@..,^OoO......=OOO. 
    ...... ^...=OO^.^.@^ =^*=^,O          \..Ooo^  ,@..=OOOO..*....OOO. 
    ...... ^...=o@^.`.O@. .  ... .. ....  ^.*`.*^  =^..o@oO@*.=....OOO^ 
    ...... ^...=oOO.*.\O   ... .......... .\   ` ,=^*.,OOOO@^.=`^..=OO\ 
    ...... ^...*`OO.*.=O ........          ......,`*^.=OOOo@^.=^^..=OOO.
    ...... \....*oO^..*O^ ....... @OO[[[`  ......../.,@OOOo@^..OO...OOO`
    ...... =.....*.=`..,O`       .O.....=   ... ^.=..OOOOO=O@..=O^..OOO^
    ...... .^...**.O@...\O^ .     \.....`   .^ /.,^.=O@OO`=O@^..OO`.=OO\
    ...... .^...,.=O=@...OO@\      ,[O\=.    ./`.*.*OOOOO..OOO*..OO.,OOO
    ....../O....../^=O@`..O@@@@@]`    .* .,/@@/..../OOOOO*.,OOO..,OO`=OO
    @OO\ooO....,*/@^,@@@\..@^[\@@@@@@O]*]//[`@^*^*=OOOOOO^..=OO\...\^.\@
    OOooo^..`./oOO@/ =^\/^.^\\....=]......,/@@^O^*O.... .,][],OO\....\`.
    @Oooo\/]OOOOOO/  .  \.=^....,..........[.,OO^=^.    /    ,`\OO`.....
    """
__version__ = "0.0.1"
__plugin_meta__ = PluginMetadata(
    name="远程同意好友",
    description='自定义远程同意好友',
    usage=logo,
    type="application",
    homepage="https://github.com/Agnes4m/nonebot_plugin_friends",
    supported_adapters={"~onebot.v11"},
    extra={
        "version": __version__,
        "author": "Agnes4m <Z735803792@163.com>",
    },
)


add_friend = on_request(Friend_, priority=1, block=True)
agree_qq_add = on_command("同意", permission=SUPERUSER)

@add_friend.handle()
async def _(bot: Bot, 
            event: FriendRequestEvent,
        ):
    logger.info('开始处理好友添加事件')
    # try:
    add_req = json.loads(event.json())
    add_qq:str = event.user_id
    add_comment = event.comment
    add_flag = event.flag
    logger.info(f'已经获取{add_qq}的好友添加事件')
    friend_request = Friend_request(
        add_id=int(add_qq), 
        add_comment=add_comment, 
        add_flag=add_flag
        )
    await save_msg(friend_request)
    realtime = time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime(add_req["time"]))
    for su_qq in super_id:
        logger.info(f'发送给{su_qq}')
        await bot.send_private_msg(
            user_id=int(su_qq),
            message=Message(f"QQ：{add_qq} 请求添加{config.bot_nickname}为好友!\n请求添加时间：{realtime}\n验证信息为：{add_comment}")
            )
        
@agree_qq_add.handle()
async def _(bot: Bot, 
            event: MessageEvent,
            matcher: Matcher,
            arg:Message = CommandArg()):
    if not arg:
        try:
            add_request =await save_msg(msg=None,fina=True)
            if add_request:
                await bot.set_friend_add_request(flag=add_request.add_flag, approve=True, remark="")
                await matcher.send("{config.bot_nickname}成功添加QQ:{add_request.add_id}为好友！")
            else:
                await matcher.send(f'已经没有好友添加拉{config.bot_nickname}')
        except Exception as E:
            await matcher.send(f"{config.bot_nickname}同意好友失败了惹\n{E}，可能是已经添加了")
    else:
        add_id = arg.extract_plain_text()
        if add_id.isdigit():
            await save_msg(int(add_id))
        else:
            await matcher.send(f"参数错误，正确格式为\n【同意11451491】")
