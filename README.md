# LittleMouseAdventure
an adventure RPG game practice
这是一个使用 Pygame 开发的简易 RPG 游戏，包含战斗、养成、抽卡、存档等功能。所有代码均为 Python 脚本，结构清晰，适合学习或扩展。


文件说明
main.py	         游戏主入口，包含主循环、事件处理、状态切换和绘制调度。
constants.py	   定义所有常量，如屏幕尺寸、颜色、字体、游戏状态、按钮尺寸、抽卡概率等。
ui.py	           所有绘制函数，包括菜单、战斗、养成、抽卡等界面的绘制。
handlers.py	     输入处理函数，处理鼠标点击事件，并根据当前状态调用相应的逻辑函数。
battle.py	       战斗逻辑，包含玩家攻击、玩家技能（治疗）、敌人攻击等函数。
levels.py	       关卡数据，根据关卡编号生成对应的敌人数据。
upgrade.py	     养成逻辑，包括使用经验书和技能书的函数。
gacha.py	       抽卡逻辑，包含角色池定义和抽卡函数（消耗金币）。
save.py	         存档与读档功能，使用 JSON 文件保存游戏进度。


运行说明
安装 Python 3.12+ 和 Pygame 库：
```bash
pip install pygame
```


运行 main.py：
```bash
python main.py
```

游戏操作
鼠标点击按钮进行选择

ESC 键返回上一级菜单

游戏特性
战斗系统：攻击、治疗、敌人 AI

角色养成：升级、学习技能

抽卡系统：消耗金币随机获得新角色

存档系统：自动保存和手动保存

