# handlers.py - 输入处理函数
import pygame


from constants import *
from battle import player_skill, reset_team_hp, get_next_attacker
from upgrade import use_exp_book, use_skill_book, toggle_active
from gacha import perform_gacha
from levels import setup_enemy
from upgrade import use_exp_book, use_skill_book, toggle_active
import formation

win_button_rect = None  


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
    
    margin = 20
    bottom_y = SCREEN_HEIGHT - MENU_BTN_HEIGHT - margin
    gacha_rect = pygame.Rect(SCREEN_WIDTH - MENU_BTN_WIDTH - margin, bottom_y, MENU_BTN_WIDTH, MENU_BTN_HEIGHT)
    if gacha_rect.collidepoint(pos):
        return STATE_GACHA

    upgrade_rect = pygame.Rect(gacha_rect.left - MENU_BTN_WIDTH - margin, bottom_y, MENU_BTN_WIDTH, MENU_BTN_HEIGHT)
    if upgrade_rect.collidepoint(pos):
        return STATE_UPGRADE

    return game_state


def handle_challenge_click(pos, game_state, current_level, player_team):
    btn_x = (SCREEN_WIDTH - BTN_WIDTH) // 2
    # 检测返回主菜单按钮
    if pygame.Rect(50, SCREEN_HEIGHT-100, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT).collidepoint(pos):
        return STATE_MENU, current_level
    # 关卡按钮
    if pygame.Rect(btn_x - 100, 350, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT).collidepoint(pos):
        return STATE_CONFIRM, 1
    elif pygame.Rect(btn_x + 150, 350, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT).collidepoint(pos):
        return STATE_CONFIRM, 2
    elif pygame.Rect(btn_x + 400, 350, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT).collidepoint(pos):
        return STATE_CONFIRM, 3
    return game_state, current_level

def find_combatant_index_by_entity(combatants, entity):
    for i, c in enumerate(combatants):
        if c["entity"] is entity:
            return i
    return None

def handle_battle_click(pos, game_state, combatants, current_index, player_team, enemies, skill_points, battle_sub_state):
    # 如果当前是敌人回合，不能操作
    if combatants[current_index]["type"] == "enemy":
        return game_state, combatants, current_index, skill_points, battle_sub_state, None

    # 按钮区域（与UI一致）
    margin = 20
    button_y = SCREEN_HEIGHT - 60 - margin
    btn_width, btn_height = 150, 60
    btn_spacing = 10
    x_attack = margin
    x_skill = x_attack + btn_width + btn_spacing
    x_run = x_skill + btn_width + btn_spacing

    # 根据子状态处理
    if battle_sub_state == BATTLE_STATE_ACTION:
        # 攻击按钮
        if pygame.Rect(x_attack, button_y, btn_width, btn_height).collidepoint(pos):
            print("选择目标...")
            return game_state, combatants, current_index, skill_points, BATTLE_STATE_TARGET, None
        # 技能按钮
        elif pygame.Rect(x_skill, button_y, btn_width, btn_height).collidepoint(pos):
            result, new_index, new_skill_points = player_skill(combatants, current_index, player_team, skill_points)
            if result == "win":
                reset_team_hp(player_team)
                return STATE_WIN, combatants, new_index, new_skill_points, battle_sub_state, None
            elif result == "no_skill":
                print("技能点不足！")
                return game_state, combatants, current_index, skill_points, battle_sub_state, None
            else:
                return game_state, combatants, new_index, new_skill_points, battle_sub_state, None
        # 逃跑按钮
        elif pygame.Rect(x_run, button_y, btn_width, btn_height).collidepoint(pos):
            reset_team_hp(player_team)
            return STATE_CHALLENGE, combatants, current_index, skill_points, battle_sub_state, None
        else:
            return game_state, combatants, current_index, skill_points, battle_sub_state, None

    elif battle_sub_state == BATTLE_STATE_TARGET:
        # 检测点击敌人（只选活着的）
        slots = formation.get_enemy_slots(enemies)
        for enemy, idx, (x, y) in slots:
            if enemy is None or enemy["hp"] <= 0:   # 跳过死亡敌人
                continue
            rect = pygame.Rect(x, y, formation.SLOT_WIDTH, formation.SLOT_HEIGHT)
            if rect.collidepoint(pos):
                target_idx = find_combatant_index_by_entity(combatants, enemy)
                if target_idx is not None:
                    print(f"选中目标 {enemy['name']}")
                    return game_state, combatants, current_index, skill_points, BATTLE_STATE_ANIM, target_idx
        return game_state, combatants, current_index, skill_points, battle_sub_state, None

    # 其他情况
    return game_state, combatants, current_index, skill_points, battle_sub_state, None

def handle_upgrade_click(pos, selected_role_index, player_team, inventory, scroll):
    """处理养成界面点击"""
    # 检测返回主菜单按钮
    menu_rect = pygame.Rect(50, SCREEN_HEIGHT-100, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT)
    if menu_rect.collidepoint(pos):
        return STATE_MENU, selected_role_index

    # 检测角色列表点击（支持滚动）
    visible_count = 6
    for i in range(visible_count):
        actual_idx = scroll + i
        if actual_idx >= len(player_team):
            break
        btn_rect = pygame.Rect(50, 150 + i * 100, 200, 80)
        if btn_rect.collidepoint(pos):
            selected_role_index = actual_idx

    # 检测切换上阵按钮
    toggle_rect = pygame.Rect(600, 550, 180, 60)
    if toggle_rect.collidepoint(pos):
        toggle_active(selected_role_index, player_team)

    # 检测经验书按钮
    exp_rect = pygame.Rect(600, 450, 180, 60)
    if exp_rect.collidepoint(pos):
        use_exp_book(selected_role_index, player_team, inventory)

    # 检测技能书按钮
    skill_rect = pygame.Rect(800, 450, 180, 60)
    if skill_rect.collidepoint(pos):
        use_skill_book(selected_role_index, player_team, inventory)

    return STATE_UPGRADE, selected_role_index

def handle_gacha_click(pos, player_team, inventory):
    """处理抽卡界面的点击，返回抽到的角色 或 "back" 表示返回"""
    btn_x = (SCREEN_WIDTH - BTN_WIDTH) // 2
    # 检测返回按钮（坐标与绘制时一致）
    back_rect = pygame.Rect(50, SCREEN_HEIGHT-100, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT)
    if back_rect.collidepoint(pos):
        return "back"
    # 检测抽卡按钮r
    if pygame.Rect(btn_x, 350, BTN_WIDTH, BTN_HEIGHT).collidepoint(pos):
        return perform_gacha(player_team, inventory)
    
    return None

def handle_save_click(pos):
    """保存点击处理"""
    btn_x = (SCREEN_WIDTH - BTN_WIDTH) // 2
    if pygame.Rect(btn_x, 450, BTN_WIDTH, BTN_HEIGHT).collidepoint(pos):
        return True  # 返回 True 表示需要保存
    return False

def handle_confirm_click(pos, level):
    """处理确认界面点击，返回 ('go', level) 或 ('back', None) 或 None"""
    btn_w, btn_h = 120, 50
    btn_y = SCREEN_HEIGHT//2 + 20
    return_rect = pygame.Rect(SCREEN_WIDTH//2 - 140, btn_y, btn_w, btn_h)
    go_rect = pygame.Rect(SCREEN_WIDTH//2 + 20, btn_y, btn_w, btn_h)
    if return_rect.collidepoint(pos):
        return ('back', None)
    elif go_rect.collidepoint(pos):
        return ('go', level)
    return None

def handle_lose_click(pos):
    """处理失败界面点击，点击确认返回 True"""
    btn_w, btn_h = 120, 50
    btn_rect = pygame.Rect(SCREEN_WIDTH//2 - btn_w//2, SCREEN_HEIGHT//2 + 20, btn_w, btn_h)
    if btn_rect.collidepoint(pos):
        return True
    return False

def handle_win_click(pos):
    """处理胜利界面点击，点击确认返回 True"""
    global win_button_rect
    if win_button_rect and win_button_rect.collidepoint(pos):
        return True
    return False