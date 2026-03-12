# characters/sheild_mouse.py
from constants import PURPLE   # 颜色常量可以从 constants 导入

ROLE_DATA = {
    "name": "盾牌鼠鼠",
    "rarity": "SR",
    "level": 1,
    "exp": 0,
    "exp_to_next": 80,
    "hp": 120,
    "max_hp": 120,
    "atk": 15,
    "stamina": 70,
    "taunt":2,
    "speed": 30,
    "skills": [
        {
            "name": "嘲讽",
            "type": "taunt",
            "target": "self",
            "value": 5,               # 增加的嘲讽值
            "description": "嘲讽敌人！",
            "level": 1,
            "proficiency": 0,
            "prof_to_next": 50
        }
    ],
    "color": PURPLE,
}
