# characters/legend_mouse.py
from constants import YELLOW   # 颜色常量可以从 constants 导入

ROLE_DATA = {
    "name": "传奇鼠鼠",
    "rarity": "SSR",
    "level": 1,
    "exp": 0,
    "exp_to_next": 80,
    "hp": 100,
    "max_hp": 100,
    "atk": 50,
    "stamina": 75,
    "taunt":1,
    "speed": 65,
    "skills": [
        {
            "name": "剑术",
            "type": "attack",          # 技能类型：heal（治疗）、attack（攻击）、buff（增益）等
            "target": "single",      # 目标类型：self（自身）、single（单体）、all（全体）
            "value": 55,             # 基础治疗量/伤害值，也可用公式
            "description": "挥舞长剑，攻击！",
            "level": 1,
            "proficiency": 0,
            "prof_to_next": 50
        }
    ],
    "color": YELLOW,
}

