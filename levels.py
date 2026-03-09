# levels.py - 关卡数据和敌人生成

# levels.py

def setup_enemy(level):
    if level == 1:
        return {"name": "史莱姆王", "hp": 200, "max_hp": 200, "atk": 25, "speed": 20}
    elif level == 2:
        return {"name": "哥布林首领", "hp": 300, "max_hp": 300, "atk": 35, "speed": 30}
    elif level == 3:
        return {"name": "龙王", "hp": 500, "max_hp": 500, "atk": 50, "speed": 40}
    else:
        return {"name": "未知敌人", "hp": 100, "max_hp": 100, "atk": 20, "speed": 25}