# levels.py

# levels.py

def setup_enemy(level):
    """返回敌人列表和初始技能点数，每个敌人指定站位索引"""
    if level == 1:
        enemies = [
            {"name": "史莱姆A", "hp": 80, "max_hp": 80, "atk": 15, "speed": 20, "slot": 0},
            {"name": "史莱姆B", "hp": 80, "max_hp": 80, "atk": 15, "speed": 20, "slot": 4},
        ]
        skill_points = 3
    elif level == 2:
        enemies = [
            {"name": "哥布林", "hp": 100, "max_hp": 100, "atk": 20, "speed": 25, "slot": 1},
            {"name": "哥布林弓箭手", "hp": 70, "max_hp": 70, "atk": 25, "speed": 30, "slot": 3},
            {"name": "哥布林首领", "hp": 150, "max_hp": 150, "atk": 30, "speed": 20, "slot": 0},
        ]
        skill_points = 2
    elif level == 3:
        enemies = [
            {"name": "龙仔", "hp": 120, "max_hp": 120, "atk": 25, "speed": 35, "slot": 0},
            {"name": "龙仔", "hp": 120, "max_hp": 120, "atk": 25, "speed": 35, "slot": 2},
            {"name": "龙王", "hp": 300, "max_hp": 300, "atk": 50, "speed": 40, "slot": 4},
        ]
        skill_points = 1
    else:
        # 默认情况（向后兼容）
        enemies = [{"name": "未知敌人", "hp": 100, "max_hp": 100, "atk": 20, "speed": 25, "slot": 0}]
        skill_points = 3
    return enemies, skill_points