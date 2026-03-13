# levels.py

# levels.py

def setup_enemy(level):
    """返回敌人列表和初始技能点数，每个敌人指定站位索引"""
    if level == 1:
        enemies = [
            {"name": "史莱姆", "hp": 800, "max_hp": 800, "atk": 150, "speed": 50, "slot": 0},
            {"name": "史莱姆", "hp": 800, "max_hp": 800, "atk": 150, "speed": 50, "slot": 4},
        ]
        skill_points = 3
    elif level == 2:
        enemies = [
            {"name": "哥布林", "hp": 1200, "max_hp": 1200, "atk": 200, "speed": 55, "slot": 0},
            {"name": "哥布林", "hp": 1200, "max_hp": 1200, "atk": 300, "speed": 60, "slot": 4},
            {"name": "哥布林", "hp": 1200, "max_hp": 1200, "atk": 200, "speed": 55, "slot": 2},
        ]
        skill_points = 2
    elif level == 3:
        enemies = [
            {"name": "哥布林", "hp": 1200, "max_hp": 1200, "atk": 300, "speed": 55, "slot": 0},
            {"name": "哥布林", "hp": 1200, "max_hp": 1200, "atk": 300, "speed": 55, "slot": 4},
            {"name": "史莱姆", "hp": 800, "max_hp": 800, "atk": 150, "speed": 60, "slot": 2},
        ]
        skill_points = 1
    else:
        # 默认情况（向后兼容）
        enemies = [{"name": "未知敌人", "hp": 1000, "max_hp": 1000, "atk": 200, "speed": 25, "slot": 0}]
        skill_points = 3
    return enemies, skill_points