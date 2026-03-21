# gacha.py - 抽卡逻辑

import random
from constants import *
from characters import load_all_roles   # 导入加载函数
from config import level_config as level_cfg

# 动态加载所有角色作为抽卡池
role_pool = load_all_roles()

def perform_gacha(player_team, inventory):
    """抽卡，需要消耗金币"""
    # 设定每次抽卡消耗 10 金币（你可以自己调整数值）
    COST = 10

    # 检查金币是否足够
    if inventory.get("gold", 0) < COST:
        print("金币不足！无法抽卡")
        return None

    # 扣除金币
    inventory["gold"] -= COST
    print(f"消耗 {COST} 金币，剩余 {inventory['gold']} 金币")

    # 抽稀有度
    rarities = list(RARITY_PROB.keys())
    rarity = random.choices(rarities, weights=list(RARITY_PROB.values()))[0]

    # 抽角色（从池里随机选匹配稀有度的）
    candidates = [r for r in role_pool if r["rarity"] == rarity]
    if candidates:
        new_role = random.choice(candidates).copy()
        new_role["exp_to_next"] = level_cfg.BASE_EXP_TO_NEXT  # 技能熟练度相关字段保持不变（如果需要配置化可后续添加）
        new_role["active"] = False          # 新角色默认不上阵
        new_role["fatigue"] = 0
        player_team.append(new_role)
        print(f"抽到 {rarity} 角色: {new_role['name']}")
        return new_role
    return None