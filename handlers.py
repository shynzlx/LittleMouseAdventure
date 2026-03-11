# handlers.py - 输入处理函数
import pygame
import ui          # 新增：访问当前按钮列表
import game        # 新增：可能用到游戏状态
from constants import *
from battle import player_skill, reset_team_hp, get_next_attacker
from upgrade import use_exp_book, use_skill_book, toggle_active
from gacha import perform_gacha
from levels import setup_enemy
import formation

def handle_ui_event(event):
    """处理UI按钮事件，返回True表示已处理"""
    for btn in ui.current_buttons:
        if btn.handle_event(event):
            return True
    return False

def handle_battle_target_click(pos):
    """处理战斗中选择目标的点击（非按钮区域）"""
    if game.game_state != STATE_CHALLENGE_BATTLE or game.battle_sub_state != BATTLE_STATE_TARGET:
        return False

    # 检测点击敌人（只选活着的）
    slots = formation.get_enemy_slots(game.enemies)
    for enemy, idx, (x, y) in slots:
        if enemy is None or enemy["hp"] <= 0:
            continue
        rect = pygame.Rect(x, y, formation.SLOT_WIDTH, formation.SLOT_HEIGHT)
        if rect.collidepoint(pos):
            target_idx = find_combatant_index_by_entity(game.combatants, enemy)
            if target_idx is not None:
                # 设置动画变量
                game.anim_attacker_idx = game.current_index
                game.anim_target_idx = target_idx
                game.anim_phase = 1
                game.anim_phase_frame = 0
                game.battle_sub_state = BATTLE_STATE_ANIM
                return True
    return False

def find_combatant_index_by_entity(combatants, entity):
    for i, c in enumerate(combatants):
        if c["entity"] is entity:
            return i
    return None

def handle_upgrade_list_click(pos):
    """养成界面点击角色列表（非按钮区域？实际上我们已用按钮处理，此函数可保留备用或删除）"""
    # 现在角色列表也是按钮，所以不需要这个函数了，但可以保留以防万一
    pass

def handle_formation_slot_click(pos):
    """处理上阵界面站位点击"""
    if game.game_state != STATE_FORMATION:
        return False

    # 计算站位区域（与 draw_formation 中一致）
    offset_x = 300
    # 获取当前上阵阵容
    active_team = game.get_active_team()
    for i, (x, y) in enumerate(formation.PLAYER_POSITIONS):
        rect = pygame.Rect(x + offset_x, y, formation.SLOT_WIDTH, formation.SLOT_HEIGHT)
        if rect.collidepoint(pos):
            # 判断该格子是否有角色
            if active_team[i] is not None:
                # 有角色 -> 下阵
                game.remove_role_from_slot(i)
                # 刷新界面（无需额外操作，下次绘制自动更新）
                return True
            else:
                # 空位，且处于选择站位阶段且有选中角色
                if game.formation_step == 1 and game.formation_selected_role_index != -1:
                    ui.place_role_to_slot(i)
                    return True
    return False
