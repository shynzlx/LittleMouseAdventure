# constants.py - 所有常量定义

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
# 主界面右下角按钮尺寸
MENU_BTN_WIDTH = 180
MENU_BTN_HEIGHT = 60
MAX_ACTIVE = 6          # 最大上阵人数

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
FONT_TITLE = "simhei.ttf", 72, True
FONT_BIG = "simhei.ttf", 48
FONT_MEDIUM = "simhei.ttf", 36
FONT_SMALL = "simhei.ttf", 28

# 状态枚举
STATE_MENU = 0
STATE_CHALLENGE = 1
STATE_CHALLENGE_BATTLE = 3    #
STATE_WORLD = 4    #大世界界面
STATE_UPGRADE = 5 #角色养成界面
STATE_GACHA = 6  # 新增抽卡界面、
STATE_CONFIRM = 7  # 关卡确认界面
STATE_LOSE = 8     #失败界面
STATE_WIN = 9   # 胜利界面

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

# 回合制战斗相关
BASE_TIME = 10000          # 计算剩余时间的基数

# 动画相关
ANIMATION_SPEED = 10       # 移动速度（像素/帧）
ANIMATION_DISTANCE = 25    # 攻击时向前移动的距离
ANIM_PHASE_FRAMES = 40      # 每阶段帧数

# 战斗子状态
BATTLE_STATE_ACTION = 0
BATTLE_STATE_TARGET = 1
BATTLE_STATE_ANIM = 2

