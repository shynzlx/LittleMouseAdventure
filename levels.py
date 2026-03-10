# levels.py

# levels.py

def setup_enemy(level):
    """返回敌人列表和初始技能点数，每个敌人指定站位索引"""
    if level == 1:
        enemies = [
            {"name": "史莱姆", "hp": 80, "max_hp": 80, "atk": 15, "speed": 50, "slot": 0},
            {"name": "史莱姆", "hp": 80, "max_hp": 80, "atk": 15, "speed": 50, "slot": 4},
        ]
        skill_points = 3
    elif level == 2:
        enemies = [
            {"name": "哥布林", "hp": 100, "max_hp": 100, "atk": 20, "speed": 55, "slot": 0},
            {"name": "哥布林", "hp": 120, "max_hp": 100, "atk": 30, "speed": 60, "slot": 4},
            {"name": "哥布林", "hp": 100, "max_hp": 100, "atk": 20, "speed": 55, "slot": 2},
        ]
        skill_points = 2
    elif level == 3:
        enemies = [
            {"name": "哥布林", "hp": 120, "max_hp": 100, "atk": 30, "speed": 55, "slot": 0},
            {"name": "哥布林", "hp": 120, "max_hp": 100, "atk": 30, "speed": 55, "slot": 4},
            {"name": "史莱姆", "hp": 80, "max_hp": 80, "atk": 15, "speed": 60, "slot": 2},
        ]
        skill_points = 1
    else:
        # 默认情况（向后兼容）
        enemies = [{"name": "未知敌人", "hp": 100, "max_hp": 100, "atk": 20, "speed": 25, "slot": 0}]
        skill_points = 3
    return enemies, skill_points