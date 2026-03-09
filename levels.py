# levels.py

def setup_enemy(level):
    """返回敌人信息和该关卡初始技能点数"""
    if level == 1:
        enemy = {"name": "史莱姆王", "hp": 200, "max_hp": 200, "atk": 25, "speed": 20}
        skill_points = 3   # 初始技能点数
    elif level == 2:
        enemy = {"name": "哥布林首领", "hp": 300, "max_hp": 300, "atk": 35, "speed": 30}
        skill_points = 2
    elif level == 3:
        enemy = {"name": "龙王", "hp": 500, "max_hp": 500, "atk": 50, "speed": 40}
        skill_points = 1
    else:
        enemy = {"name": "未知敌人", "hp": 100, "max_hp": 100, "atk": 20, "speed": 25}
        skill_points = 3
    return enemy, skill_points