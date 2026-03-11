# handlers.py - 输入处理函数
import pygame
import ui          # 新增：访问当前按钮列表
import game        # 新增：可能用到游戏状态
from constants import *
from battle import reset_team_hp, get_next_attacker, use_skill
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
    if game.game_state != STATE_CHALLENGE_BATTLE or not game.target_selection_mode:
        return False

    # ---------- 普通攻击（无 pending_skill）----------
    if game.pending_skill is None:
        from formation import get_enemy_slots, SLOT_WIDTH, SLOT_HEIGHT
        slots = get_enemy_slots(game.enemies)
        for enemy, slot_idx, (x, y) in slots:
            if enemy is None or enemy["hp"] <= 0:
                continue
            rect = pygame.Rect(x, y, SLOT_WIDTH, SLOT_HEIGHT)
            if rect.collidepoint(pos):
                # 找到该敌人在 combatants 中的索引
                target_idx = find_combatant_index_by_entity(game.combatants, enemy)
                if target_idx is not None:
                    # 设置动画
                    game.anim_is_skill = False
                    game.anim_attacker_idx = game.current_index
                    game.anim_target_idx = target_idx
                    game.anim_phase = 1
                    game.anim_phase_frame = 0
                    game.battle_sub_state = BATTLE_STATE_ANIM
                    # 退出目标选择模式
                    game.target_selection_mode = False
                    return True
        return False

    # ---------- 技能攻击 ----------
    skill = game.pending_skill
    if not skill:
        return False

    if skill["type"] == "heal" and skill["target"] == "single":
        from formation import get_player_slots, SLOT_WIDTH, SLOT_HEIGHT
        active_team = game.get_active_team()
        slots = get_player_slots(active_team)
        for role, slot_idx, (x, y) in slots:
            if role is None or role["hp"] <= 0:
                continue
            rect = pygame.Rect(x, y, SLOT_WIDTH, SLOT_HEIGHT)
            if rect.collidepoint(pos):
                # 找到该角色在 player_team 中的索引
                target_idx = next((i for i, r in enumerate(game.player_team) if r is role), None)
                if target_idx is not None:
                    # 找到该角色在 combatants 中的索引（用于动画目标）
                    target_combatant_idx = find_combatant_index_by_entity(game.combatants, role)
                    if target_combatant_idx is None:
                        continue
                    # 存储技能信息，准备动画
                    game.anim_is_skill = True  
                    game.anim_skill = skill
                    game.anim_skill_target_idx = target_idx
                    game.anim_attacker_idx = game.current_index
                    game.anim_target_idx = target_combatant_idx
                    game.anim_phase = 1
                    game.anim_phase_frame = 0
                    game.battle_sub_state = BATTLE_STATE_ANIM
                    game.target_selection_mode = False
                    game.pending_skill = None
                    return True

    elif skill["type"] == "attack" and skill["target"] == "single":
        from formation import get_enemy_slots, SLOT_WIDTH, SLOT_HEIGHT
        slots = get_enemy_slots(game.enemies)
        for enemy, slot_idx, (x, y) in slots:
            if enemy is None or enemy["hp"] <= 0:
                continue
            rect = pygame.Rect(x, y, SLOT_WIDTH, SLOT_HEIGHT)
            if rect.collidepoint(pos):
                # 找到该敌人在 enemies 中的索引
                target_idx = next((i for i, e in enumerate(game.enemies) if e is enemy), None)
                if target_idx is not None:
                    # 找到该敌人在 combatants 中的索引（用于动画目标）
                    target_combatant_idx = find_combatant_index_by_entity(game.combatants, enemy)
                    if target_combatant_idx is None:
                        continue
                    # 存储技能信息，准备动画
                    game.anim_is_skill = True
                    game.anim_skill = skill
                    game.anim_skill_target_idx = target_idx
                    game.anim_attacker_idx = game.current_index
                    game.anim_target_idx = target_combatant_idx
                    game.anim_phase = 1
                    game.anim_phase_frame = 0
                    game.battle_sub_state = BATTLE_STATE_ANIM
                    game.target_selection_mode = False
                    game.pending_skill = None
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
