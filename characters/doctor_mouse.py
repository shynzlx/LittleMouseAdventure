# characters/doctor_mouse.py
from constants import BLUE   # 颜色常量可以从 constants 导入

ROLE_DATA = {
    "name": "医生鼠鼠",
    "rarity": "R",
    "level": 1,
    "exp": 0,
    "hp": 900,
    "max_hp": 900,
    "atk": 100,
    "stamina": 750,
    "taunt":1,
    "speed": 45,
    "skills": [
        {
            "name": "治疗",
            "type": "heal",          # 技能类型：heal（治疗）、attack（攻击）、buff（增益）等
            "target": "single",      # 目标类型：self（自身）、single（单体）、all（全体）
            "value": 350,             # 基础治疗量/伤害值，也可用公式
            "description": "为一名队友恢复350点生命值",
            "level": 1,
            "proficiency": 0,
            "prof_to_next": 1000
        }
    ],
    "color": BLUE,
}
