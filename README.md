<!-- markdownlint-disable MD026 MD031 MD033 MD036 MD041 MD046 MD051 MD050-->
<div align="center">
  <img src="https://raw.githubusercontent.com/Agnes4m/nonebot_plugin_l4d2_server/main/image/logo.png" width="180" height="180"  alt="AgnesDigitalLogo">
  <br>
  <p><img src="https://s2.loli.net/2022/06/16/xsVUGRrkbn1ljTD.png" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot_plugin_friends

__✨Nonebot同意好友✨__

<a href="https://github.com/Agnes4m/nonebot_plugin_friends/stargazers">
        <img alt="GitHub stars" src="https://img.shields.io/github/stars/Agnes4m/nonebot_plugin_friends" alt="stars">
</a>
<a href="https://github.com/Agnes4m/nonebot_plugin_friends/issues">
        <img alt="GitHub issues" src="https://img.shields.io/github/issues/Agnes4m/nonebot_plugin_friends" alt="issues">
</a>
<a href="https://jq.qq.com/?_wv=1027&k=HdjoCcAe">
        <img src="https://img.shields.io/badge/QQ%E7%BE%A4-399365126-orange?style=flat-square" alt="QQ Chat Group">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_friends">
        <img src="https://img.shields.io/pypi/v/nonebot_plugin_friends.svg" alt="pypi">
</a>
    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
    <img src="https://img.shields.io/badge/nonebot-2.0.0-red.svg" alt="NoneBot">
</div>

## 安装

以下提到的方法 任选**其一**即可

<details open>
<summary>[推荐] 使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

```bash
nb plugin install nonebot_plugin_friends
```

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

```bash
pip install nonebot_plugin_friends
```

</details>
<details>
<summary>pdm</summary>

```bash
pdm add nonebot_plugin_friends
```

</details>
<details>
<summary>poetry</summary>

```bash
poetry add nonebot_plugin_friends
```

</details>
<details>
<summary>conda</summary>

```bash
conda install nonebot_plugin_friends
```

</details>
</details>

## 指令

### 好友申请（权限为master_id|SUPERUSER）

- (被动) —— 接受好友请求
- 同意 —— 同意最近一次好友请求
- 同意[number] —— 同意指定qq号添加好友
- (回复消息)同意 —— 同意改申请的对象

### 群聊申请(权限为群主|管理|master_id|SUPERUSER)

- (被动) —— 接受群聊申请
- 同意[number] —— 同意指定qq号添加好友
- (回复消息)同意 —— 同意改申请的对象

## env配置

不知道可以不写
知道就按下面参数改添加到env中

    bot_nickname = '宁宁'
    master_nickname = '主人'
    master_id = ['114514']
    group_request = True      # 开启群聊申请处理

## 🙈 其他

- 本项目仅供学习使用，请勿用于商业用途，喜欢该项目可以Star或者提供PR
- [爱发电](https://afdian.net/a/agnes_digital)
