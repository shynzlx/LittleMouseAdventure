# config/skill_config.py
# 技能升级配置，用于平衡性调整

# 技能熟练度增加范围（每次使用技能书增加的熟练度）
SKILL_PROFICIENCY_GAIN_MIN = 30
SKILL_PROFICIENCY_GAIN_MAX = 50  # 实际增加值为 min + random(0, max-min)

# 攻击和治疗技能每次升级增加的效果值
ATTACK_HEAL_UPGRADE_VALUE_INCREASE = 5

# 嘲讽技能每次升级增加的效果值（嘲讽值增量）
TAUNT_UPGRADE_VALUE_INCREASE = 2

# 嘲讽技能升级时回复自身最大生命值的比例（0.15 = 15%）
TAUNT_UPGRADE_HEAL_RATIO = 0.15

# 其他技能类型默认增加的效果值（如果不属于以上类型）
DEFAULT_UPGRADE_VALUE_INCREASE = 5