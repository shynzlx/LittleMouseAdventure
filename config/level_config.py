# config/level_config.py
# 角色升级通用配置

# 使用经验书时获得的经验范围（最小值，最大值）
EXP_BOOK_GAIN_MIN = 8000
EXP_BOOK_GAIN_MAX = 12000  # 实际获得为 min + random(0, max-min)

# 下一级经验倍率（每次升级后，exp_to_next = exp_to_next * FACTOR）
NEXT_LEVEL_EXP_FACTOR = 1.05

# 角色从等级1升到2所需的基础经验（所有角色统一）
BASE_EXP_TO_NEXT = 800

# 升级时属性增加量
LEVEL_UP_HP_INCREASE = 15
LEVEL_UP_ATK_INCREASE = 5
LEVEL_UP_STAMINA_INCREASE = 8