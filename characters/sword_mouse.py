# characters/sword_mouse.py
from constants import BLUE  # 颜色常量可以从 constants 导入

ROLE_DATA = {
    "name": "短剑鼠鼠",
    "rarity": "R",
    "level": 1,
    "exp": 0,
    "hp": 800,
    "max_hp": 800,
    "atk": 400,
    "stamina": 450,
    "taunt":1,
    "speed": 50,
    "skills": [
        {
            "name": "剑术",
            "type": "attack",          # 技能类型：heal（治疗）、attack（攻击）、buff（增益）等
            "target": "single",      # 目标类型：self（自身）、single（单体）、all（全体）
            "value": 550,             # 基础治疗量/伤害值，也可用公式
            "description": "挥舞长剑，攻击！",
            "level": 1,
            "proficiency": 0,
            "prof_to_next": 500
        }
    ],
    "color": BLUE,
}
