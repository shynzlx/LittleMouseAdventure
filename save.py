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
    保存前移除每个角色的 fatigue 字段，因为疲劳只在战斗中存在，不应持久化。
    """
    # 复制队伍并移除 fatigue 字段
    team_to_save = []
    for role in player_team:
        role_copy = role.copy()          # 浅拷贝，确保不修改原对象
        role_copy.pop("fatigue", None)   # 删除 fatigue 字段（如果有）
        # 同时可考虑移除其他临时字段（如 anim_* 等），但那些不在角色数据中，不用管
        team_to_save.append(role_copy)

    data = {
        "player_team": team_to_save,
        "inventory": inventory,
        "current_level": current_level
    }

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