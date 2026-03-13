# characters/sheild_mouse.py
from constants import PURPLE   # 颜色常量可以从 constants 导入

ROLE_DATA = {
    "name": "盾牌鼠鼠",
    "rarity": "SR",
    "level": 1,
    "exp": 0,
    "hp": 1200,
    "max_hp": 1200,
    "atk": 150,
    "stamina": 700,
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
            "prof_to_next": 500
        }
    ],
    "color": PURPLE,
}
