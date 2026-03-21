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
    "stamina": 200,
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
            "prof_to_next": 500
        }
    ],
    "color": BLUE,
    "story": "  医生从来都不是鼠鼠的 “正经差事”。\n  在她还是只小小鼠的时候，就总爱蹲在角落，给受伤的伙伴们包扎伤口。\
家里几乎所有人都反对她走这条路，唯独爷爷支持。爷爷也曾是一名医生，当年给受伤的小猫包扎，却被咬掉了半截尾巴——这也是大家不看好医生这个职业的原因。\n  医生鼠鼠小时候最爱的游戏，就是扮演小医生。爷爷会把自己当年的白大褂披在她身上，轻轻裹住小小的她。\
后来王国遭遇入侵，她毫不犹豫扛起了军医的责任。每当被问起为什么一定要来前线，她总会微笑，坚毅从她笑眯眯的眼睛中映出来，并说出那句从小念到大、觉得最帅气的话：\n  “救死扶伤，是医生的职责！”",
}
