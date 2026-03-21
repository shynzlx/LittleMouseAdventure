# levels.py

from characters import load_enemy_base

def create_enemy_from_base(base, level, slot):
    """根据敌人基础数据和等级生成敌人实例"""
    stats = base["base_stats"]
    growth = base["growth"]
    hp = stats["hp"] + growth.get("hp", 0) * (level - 1)
    atk = stats["atk"] + growth.get("atk", 0) * (level - 1)
    speed = stats["speed"] + growth.get("speed", 0) * (level - 1)
    enemy = {
        "name": base["name"],
        "hp": hp,
        "max_hp": hp,
        "atk": atk,
        "speed": speed,
        "level": level,
        "slot": slot,
        "skills": [skill.copy() for skill in base.get("skills", [])],
        "stamina": base.get("stamina", 50),   # 从 base 中读取 stamina
        "fatigue": 0,
    }
    return enemy

def setup_enemy(level):
    """返回敌人列表和初始技能点数，每个敌人指定站位索引"""
    if level == 1:
        enemies_info = [
            {"name": "史莱姆", "level": 1, "slot": 0},
            {"name": "史莱姆", "level": 1, "slot": 4},
        ]
        skill_points = 3
        exp_reward = 20  
    elif level == 2:
        enemies_info = [
            {"name": "哥布林", "level": 2, "slot": 0},
            {"name": "哥布林", "level": 2, "slot": 4},
            {"name": "哥布林", "level": 2, "slot": 2},
        ]
        skill_points = 2
        exp_reward = 30
    elif level == 3:
        enemies_info = [
            {"name": "哥布林", "level": 3, "slot": 0},
            {"name": "哥布林", "level": 3, "slot": 4},
            {"name": "史莱姆", "level": 2, "slot": 2},
        ]
        skill_points = 1
        exp_reward = 40  
    else:
        # 默认情况（向后兼容）
        enemies_info = [{"name": "未知敌人", "level": 1, "slot": 0}]
        skill_points = 3
        exp_reward = 50  

    enemies = []
    for info in enemies_info:
        base = load_enemy_base(info["name"])
        if base:
            enemy = create_enemy_from_base(base, info["level"], info["slot"])
            enemies.append(enemy)
        else:
            print(f"警告：找不到敌人 {info['name']} 的基础数据，跳过。")
    return enemies, skill_points, exp_reward