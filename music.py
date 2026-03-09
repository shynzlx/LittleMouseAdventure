# music.py
from constants import *

# 界面状态到音乐文件的映射
# 键为状态常量，值为音乐文件名（相对于 assets/music/ 目录）
MUSIC_MAP = {
    STATE_MENU: "main.mp3",               # 主菜单
    STATE_CHALLENGE_BATTLE: "battle.mp3", # 战斗界面
    STATE_CHALLENGE: "challenge.mp3",    # 选关界面
    # STATE_UPGRADE: "upgrade.mp3",        # 养成界面
    # STATE_GACHA: "gacha.mp3",            # 抽卡界面
    # STATE_WORLD: "world.mp3",            # 大世界
}

def get_music_for_state(state):
    """根据游戏状态返回对应的音乐文件名，若无映射则返回 None"""
    return MUSIC_MAP.get(state)