# save.py
# 这个文件专门负责保存和加载游戏进度
# 用 JSON 文件保存，很简单可靠

import json  # Python 自带的 JSON 工具
import os    # 检查文件是否存在用
from characters import load_all_roles   # 导入角色文件
from config import level_config as level_cfg

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
    if os.path.exists(SAVE_FILE):
        # 有存档：读取存档（保持不变）
        with open(SAVE_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
        player_team = data.get("player_team", [])
        inventory = data.get("inventory", {"gold": 1000, "exp_book": 5, "skill_book": 3})
        current_level = data.get("current_level", 1)
        return player_team, inventory, current_level
    else:
        # 无存档：从角色文件创建初始队伍
        print("没有找到存档，从角色文件创建初始队伍")
        all_roles = load_all_roles()
        target_role_name = "警卫鼠鼠"
        base_role = next((r for r in all_roles if r["name"] == target_role_name), None)
        
        if base_role:
            initial_role = base_role.copy()
            initial_role["skills"] = [skill.copy() for skill in initial_role.get("skills", [])]
            # 设置初始经验值为配置值（覆盖可能存在的旧值）
            initial_role["exp_to_next"] = level_cfg.BASE_EXP_TO_NEXT
            initial_role.setdefault("active", True)
            initial_role.setdefault("speed", initial_role.get("stamina", 50))
            initial_role.setdefault("slot", 0)
            player_team = [initial_role]
            print(f"初始角色设为：{target_role_name}")
        inventory = {"gold": 1000, "exp_book": 1000, "skill_book": 1000}
        current_level = 1
        return player_team, inventory, current_level