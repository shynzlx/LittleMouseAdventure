# music.py - 音乐管理模块
import pygame
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

# 当前播放的音乐文件名
current_music = None

def get_music_for_state(state):
    """根据游戏状态返回对应的音乐文件名，若无映射则返回 None"""
    return MUSIC_MAP.get(state)

def play_music(filename, volume=0.5):
    """播放指定音乐文件（assets/music/ 下）"""
    global current_music
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(f"assets/music/{filename}")
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)
        current_music = filename
        print(f"播放音乐: {filename}")
    except Exception as e:
        print(f"音乐加载失败 {filename}: {e}")

def update_music(state):
    """根据游戏状态更新音乐"""
    music_file = get_music_for_state(state)
    if music_file and music_file != current_music:
        play_music(music_file)