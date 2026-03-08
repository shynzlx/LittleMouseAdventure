# handlers.py - 输入处理函数
import pygame


from constants import *
from battle import player_attack, player_skill
from upgrade import use_exp_book, use_skill_book
from gacha import perform_gacha
from levels import setup_enemy

def handle_menu_click(pos, game_state):
    btn_x = (SCREEN_WIDTH - BTN_WIDTH) // 2
    
    # 闯关模式
    if pygame.Rect(btn_x, 250, BTN_WIDTH, BTN_HEIGHT).collidepoint(pos):
        return STATE_CHALLENGE
    # 保存游戏
    if pygame.Rect(btn_x, 400, BTN_WIDTH, BTN_HEIGHT).collidepoint(pos):
        return "save"  # 特殊信号：保存
    # 大世界
    if pygame.Rect(btn_x, 550, BTN_WIDTH, BTN_HEIGHT).collidepoint(pos):
        return STATE_WORLD
    
    return game_state


def handle_challenge_click(pos, game_state, current_level, player_team):
    btn_x = (SCREEN_WIDTH - BTN_WIDTH) // 2
    if pygame.Rect(btn_x - 100, 350, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT).collidepoint(pos):
        # 不再调用 setup_enemy，只返回新状态和关卡
        return STATE_CHALLENGE_BATTLE, 1
    elif pygame.Rect(btn_x + 150, 350, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT).collidepoint(pos):
        return STATE_CHALLENGE_BATTLE, 2
    elif pygame.Rect(btn_x + 400, 350, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT).collidepoint(pos):
        return STATE_CHALLENGE_BATTLE, 3
    elif pygame.Rect(btn_x, 500, BTN_WIDTH, BTN_SMALL_HEIGHT).collidepoint(pos):
        return STATE_UPGRADE, current_level
    elif pygame.Rect(btn_x, 600, BTN_WIDTH, BTN_SMALL_HEIGHT).collidepoint(pos):
        return STATE_GACHA, current_level
    return game_state, current_level


def handle_battle_click(pos, game_state, player_team, enemy, battle_turn):
    """处理战斗界面的点击"""
    print(f"战斗点击: 位置 {pos}")  # 调试输出
    if 100 < pos[0] < 250 and 500 < pos[1] < 560:
        print("点击了攻击按钮")
        game_state, battle_turn = player_attack(player_team, enemy, game_state, battle_turn)
    elif 300 < pos[0] < 450 and 500 < pos[1] < 560:
        print("点击了技能按钮")
        game_state, battle_turn = player_skill(player_team, game_state, battle_turn)
    elif 500 < pos[0] < 650 and 500 < pos[1] < 560:
        print("点击了逃跑按钮")
        game_state = STATE_CHALLENGE
    return game_state, battle_turn

def handle_upgrade_click(pos, selected_role_index, player_team, inventory):
    # 切换角色
    for i in range(len(player_team)):
        if pygame.Rect(50, 150 + i*100, 200, 80).collidepoint(pos):
            selected_role_index = i

    # 使用道具
    if 600 < pos[0] < 780 and 500 < pos[1] < 560:
        use_exp_book(selected_role_index, player_team, inventory)
    elif 800 < pos[0] < 980 and 500 < pos[1] < 560:
        use_skill_book(selected_role_index, player_team, inventory)
    return selected_role_index

def handle_gacha_click(pos, player_team, inventory):
    """处理抽卡界面的点击，返回抽到的角色（如果有）"""
    btn_x = (SCREEN_WIDTH - BTN_WIDTH) // 2
    if pygame.Rect(btn_x, 350, BTN_WIDTH, BTN_HEIGHT).collidepoint(pos):
        return perform_gacha(player_team, inventory)  # 传入 inventory
    return None

def handle_save_click(pos):
    """保存点击处理"""
    btn_x = (SCREEN_WIDTH - BTN_WIDTH) // 2
    if pygame.Rect(btn_x, 450, BTN_WIDTH, BTN_HEIGHT).collidepoint(pos):
        return True  # 返回 True 表示需要保存
    return False