# gacha.py - 抽卡逻辑

import random
from constants import *

# 角色池（示例，扩展时可加更多）
role_pool = [
    {"name": "一般鼠鼠", "rarity": "N", "level": 1, "exp": 0, "exp_to_next": 80, "hp": 100, "max_hp": 100, "atk": 20, "stamina": 60, "skills": [], "color": GRAY},
    {"name": "稀有鼠鼠", "rarity": "R", "level": 1, "exp": 0, "exp_to_next": 100, "hp": 70, "max_hp": 70, "atk": 40, "stamina": 45, "skills": [{"name": "冰箭", "level": 1, "proficiency": 0, "prof_to_next": 50}], "color": BLUE},
    {"name": "聪明鼠鼠", "rarity": "SR", "level": 1, "exp": 0, "exp_to_next": 120, "hp": 110, "max_hp": 110, "atk": 10, "stamina": 70, "skills": [{"name": "神愈", "level": 1, "proficiency": 0, "prof_to_next": 60}], "color": YELLOW},
    {"name": "传奇鼠鼠", "rarity": "SSR", "level": 1, "exp": 0, "exp_to_next": 150, "hp": 200, "max_hp": 200, "atk": 50, "stamina": 90, "skills": [{"name": "圣剑", "level": 1, "proficiency": 0, "prof_to_next": 80}], "color": PURPLE}
]

def perform_gacha(player_team, inventory):
    """抽卡，需要消耗金币"""
    # 设定每次抽卡消耗 100 金币（你可以自己调整数值）
    COST = 100

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
        player_team.append(new_role)
        print(f"抽到 {rarity} 角色: {new_role['name']}")
        return new_role
    return None