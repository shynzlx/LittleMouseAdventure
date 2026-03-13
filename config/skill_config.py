# config/skill_config.py
import math  # 若需要使用 math.log, math.exp 等

# 技能熟练度增加范围
SKILL_PROFICIENCY_GAIN_MIN = 30
SKILL_PROFICIENCY_GAIN_MAX = 50

# 嘲讽技能升级时回复自身最大生命值的比例
TAUNT_UPGRADE_HEAL_RATIO = 0.15

# 技能增量公式（根据当前等级计算本次升级应增加的值）
# 变量 level 为技能当前等级（升级前的等级）
INCREMENT_FORMULAS = {
    # 攻击技能：5级前每级+30，5级后每级+ 30 * (0.95 ** (level - 4))
    # 说明：当 level=5 时，index = 1，增量 = 3 * 0.9 ≈ 2.7
    "attack": "30 if level < 5 else 30 * (0.95 ** (level - 4))",
    
    # 治疗技能：5级前每级+20，5级后每级+ 20 * (0.85 ** (level - 4))
    "heal": "20 if level < 5 else 20 * (0.85 ** (level - 4))",
    
    # 嘲讽技能：固定每级+2，不受等级影响（也可改为指数）
    "taunt": "1",

}