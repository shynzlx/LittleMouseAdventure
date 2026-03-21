# characters/general_mouse.py
from constants import GRAY   # 颜色常量可以从 constants 导入

ROLE_DATA = {
    "name": "警卫鼠鼠",
    "rarity": "N",
    "level": 1,
    "exp": 0,
    "hp": 700,
    "max_hp": 700,
    "atk": 200,
    "stamina": 500,
    "taunt": 1,
    "speed": 50,
    "skills": [
        {
            "name": "重击",
            "type": "attack",          # 技能类型：heal（治疗）、attack（攻击）、buff（增益）等
            "target": "single",      # 目标类型：self（自身）、single（单体）、all（全体）
            "value": 350,             # 基础治疗量/伤害值，也可用公式
            "description": "对敌方单体造成精确打击！",
            "level": 1,
            "proficiency": 0,
            "prof_to_next": 500
        }
    ],
    "color": GRAY,
    "story":"  他曾是稀里糊涂的来到战场上的。\n  警卫鼠鼠曾经没有考上大学，也本对自己的鼠生不报任何期待。\
直到王国被入侵的那天，他从一只哥布林手下抢过了一只小鼠的生命，这让他看到了他生命的意义——他要用手里这支小小的警棍，保卫更多的生命。"
}