# inventory.py - 关卡奖励映射

REWARD_MAP = {
    1: {"gold": 100, "exp_book": 1, "skill_book": 0},
    2: {"gold": 150, "exp_book": 1, "skill_book": 1},
    3: {"gold": 200, "exp_book": 2, "skill_book": 1},
    # 可以继续添加更多关卡
}

def get_reward_for_level(level):
    """根据关卡编号返回奖励字典，若没有则返回默认奖励"""
    return REWARD_MAP.get(level, {"gold": 50, "exp_book": 0, "skill_book": 0})