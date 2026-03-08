# save.py
# 这个文件专门负责保存和加载游戏进度
# 用 JSON 文件保存，很简单可靠

import json  # Python 自带的 JSON 工具
import os    # 检查文件是否存在用

SAVE_FILE = "save.json"  # 存档文件名，就叫 save.json，放在游戏同目录

def save_game(player_team, inventory, current_level):
    """
    把游戏数据保存到 save.json 文件
    player_team: 所有角色列表
    inventory: 背包（金币、经验书等）
    current_level: 当前关卡
    """
    # 把要保存的东西打包成一个字典
    data = {
        "player_team": player_team,          # 角色列表（字典列表）
        "inventory": inventory,              # 背包
        "current_level": current_level       # 当前关卡
    }

    # 写入文件，用 utf-8 编码支持中文
    with open(SAVE_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print("游戏已保存到 save.json 文件！")


def load_game():
    """
    从 save.json 加载游戏数据
    如果文件不存在，就返回默认值（新玩家）
    返回三个东西：player_team, inventory, current_level
    """
    # 先检查文件存不存在
    if os.path.exists(SAVE_FILE):
        # 文件存在 → 读取
        with open(SAVE_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)

        print("从 save.json 加载了存档！")

        # 取出数据，如果某项没有就用默认值
        player_team = data.get("player_team", [])
        inventory = data.get("inventory", {"gold": 1000, "exp_book": 5, "skill_book": 3})
        current_level = data.get("current_level", 1)

        return player_team, inventory, current_level

    else:
        # 文件不存在 → 新玩家，用默认数据
        print("没有找到存档，使用默认数据开始新游戏")

        # 默认初始数据
        default_team = [
            {
                "name": "战士",
                "level": 1,
                "exp": 0,
                "exp_to_next": 100,
                "hp": 150,
                "max_hp": 150,
                "atk": 30,
                "stamina": 80,
                "rarity": "R",
                "skills": [
                    {"name": "重击", "level": 1, "proficiency": 0, "prof_to_next": 50}
                ],
                "color": (255, 50, 50)  # RED
            }
        ]

        default_inventory = {
            "gold": 1000,
            "exp_book": 5,
            "skill_book": 3
        }

        return default_team, default_inventory, 1