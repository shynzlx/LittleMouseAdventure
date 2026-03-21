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
    "stamina": 800,
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
    "story":"  你可能不相信，盾牌鼠鼠其实并不是士兵。\n  他在战争爆发前是一家盾牌公司的销售员，战争爆发的那一天，他稀里糊涂的进入了正在交战的街区。\
几只被追杀而受伤的士兵鼠鼠躲在了他的后面。可能是受到幸运女神的眷顾，也可能是见过很多客户使用盾牌。他成功地在援军到达的时候防住了几轮进攻\n  “没\
吃过奶酪，还没见过奶酪机嘛！”，他的信心大增，于是踏上了保卫王国的道路。"
}
