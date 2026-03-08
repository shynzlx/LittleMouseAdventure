# constants.py - 所有常量定义

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
GREEN = (0, 200, 0)
RED = (255, 50, 50)
BLUE = (50, 150, 255)
YELLOW = (255, 255, 0)
PURPLE = (200, 100, 255)
ORANGE = (255, 165, 0)

# 字体
FONT_TITLE = "SimHei", 72, True
FONT_BIG = "SimHei", 48
FONT_MEDIUM = "SimHei", 36
FONT_SMALL = "SimHei", 28

# 状态枚举
STATE_MENU = 0
STATE_CHALLENGE = 1
STATE_CHALLENGE_BATTLE = 3
STATE_WORLD = 4
STATE_UPGRADE = 5
STATE_GACHA = 6  # 新增抽卡界面

# 按钮大小
BTN_WIDTH = 450
BTN_HEIGHT = 120
BTN_SMALL_WIDTH = 200
BTN_SMALL_HEIGHT = 80

# 稀有度概率（抽卡用）
RARITY_PROB = {
    "N": 0.5, "R": 0.3, "SR": 0.15, "SSR": 0.05
}

# 金币显示位置
GOLD_POS_X = SCREEN_WIDTH - 200
GOLD_POS_Y = 20

#初始角色
ROLES = [
    {
        "name": "战士",
        "level": 1,
        "exp": 0,
        "exp_to_next": 100,
        "hp": 150,
        "max_hp": 150,
        "atk": 30,
        "stamina": 80,
        "rarity": "R",
        "skills": [
            {"name": "重击", "level": 1, "proficiency": 0, "prof_to_next": 50}
        ],
        "color": RED
    }
]