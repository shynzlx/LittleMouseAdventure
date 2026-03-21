# main.py - 游戏主入口和主循环

import pygame
import sys
import game          # 导入全局状态
import ui
import handlers
import music
import random        # 仍然需要
from constants import *
from battle import enemy_attack, perform_attack, reset_team_hp
from inventory import get_reward_for_level
from utils import resource_path


# 初始化 Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("鼠鼠大冒险")
clock = pygame.time.Clock()

# 加载存档（启动时自动执行）
game.init_game()

# 播放当前状态音乐
music.update_music(game.game_state)

# 主循环
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:          # 关闭窗口事件
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:   # 鼠标按键按下（左键）
            if event.button in (4, 5):
                continue

            ## 第一步：让UI按钮处理（关键！）
            if handlers.handle_ui_event(event):
                continue  # 按钮已处理，跳过后续
            
            # 第二步：处理非按钮点击（如战斗选目标、上阵站位点击）
            if game.game_state == STATE_MINING:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    handlers.handle_mining_click(event.pos)
            elif game.game_state == STATE_CHALLENGE_BATTLE:
                handlers.handle_battle_target_click(event.pos)
            elif game.game_state == STATE_FORMATION:
                handlers.handle_formation_slot_click(event.pos)

        elif event.type == pygame.MOUSEWHEEL:     # 鼠标滚轮事件
            if game.game_state == STATE_UPGRADE:       # 仅在养成界面响应滚轮
                game.upgrade_scroll -= event.y
                visible_count = 7  # 养成界面一次显示7个
                max_scroll = max(0, len(game.player_team) - visible_count)
                game.upgrade_scroll = max(0, min(game.upgrade_scroll, max_scroll))
            elif game.game_state == STATE_FORMATION:
                # 上阵界面滚动角色列表
                game.formation_scroll -= event.y
                visible_count = 7  # 上阵界面一次显示7个
                max_scroll = max(0, len(game.player_team) - visible_count)
                game.formation_scroll = max(0, min(game.formation_scroll, max_scroll))
    # ESC 返回上一级
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        if game.game_state == STATE_CHALLENGE:
            game.set_state(STATE_MENU)
        elif game.game_state == STATE_WORLD:
            game.set_state(STATE_MENU)
        elif game.game_state == STATE_MINING:   
            game.set_state(STATE_MENU)

    # ===== 自动敌人攻击 =====
    if game.game_state == STATE_CHALLENGE_BATTLE and game.combatants and game.battle_sub_state == BATTLE_STATE_ACTION:
        current = game.combatants[game.current_index]
        if current["type"] == "enemy":
            from battle import calculate_taunt_probabilities  # 确保导入
            probs = calculate_taunt_probabilities(game.combatants)
            if not probs:
                game.set_state(STATE_LOSE)
            else:
                target_idx = random.choices(list(probs.keys()), weights=list(probs.values()))[0]
                # 设置动画变量
                game.anim_attacker_idx = game.current_index
                game.anim_target_idx = target_idx
                game.anim_phase = 1
                game.anim_phase_frame = 0
                game.battle_sub_state = BATTLE_STATE_ANIM

    # ===== 动画处理 =====
    # ===== 回合制战斗动画更新 =====
    if game.game_state == STATE_CHALLENGE_BATTLE and game.battle_sub_state == BATTLE_STATE_ANIM:
        game.anim_phase_frame += 1
        if game.anim_phase_frame >= ANIM_PHASE_FRAMES:
            game.anim_phase_frame = 0
            game.anim_phase += 1
            if game.anim_phase > 4:
                # 动画结束，执行实际效果
                if game.anim_skill is not None:
                    # 技能
                    from battle import use_skill
                    result, next_index, new_skill_points, _, _ = use_skill(
                        game.combatants, game.anim_attacker_idx, game.player_team, game.enemies, game.anim_skill_target_idx)
                    game.current_skill_points = new_skill_points
                    # 清空技能动画相关变量
                    game.anim_skill = None
                    game.anim_skill_target_idx = None
                else:
                    # 普通攻击
                    attacker_type = game.combatants[game.anim_attacker_idx]["type"]
                    if attacker_type == "player":
                        result, next_index, new_skill_points = perform_attack(
                            game.combatants, game.anim_attacker_idx, game.anim_target_idx, game.current_skill_points)
                        game.current_skill_points = new_skill_points
                    else:  # enemy
                        result, next_index = enemy_attack(game.combatants, game.anim_attacker_idx, game.anim_target_idx)

                # 处理战斗结果
                if result == "win":
                    game.battle_messages.clear()
                    reward = get_reward_for_level(game.current_level)
                    game.win_reward = reward
                    game.add_reward(reward)
                    # 战斗胜利经验奖励
                    active_team = game.get_active_team()
                    for role in active_team:
                        if role is not None:
                            from upgrade import add_exp_to_role
                            add_exp_to_role(role, game.current_exp_reward)
                    game.set_state(STATE_WIN)
                elif result == "lose":
                    game.battle_messages.clear()
                    game.set_state(STATE_LOSE)
                else:
                    game.current_index = next_index

                # 重置动画状态
                game.battle_sub_state = BATTLE_STATE_ACTION
                game.anim_phase = 0
                game.anim_attacker_idx = None
                game.anim_target_idx = None
                game.anim_is_skill = False
                game.anim_mode = "move" 
    game.update_damage_numbers()   # 更新伤害数字动画
    # 更新挖矿背景计时器
    if game.mining_bg_timer > 0:
        game.mining_bg_timer -= 1

    # ===== 检测状态变化并更新音乐 =====
    if game.game_state != game.prev_state:
        music.update_music(game.game_state)
        game.prev_state = game.game_state
        if game.game_state == STATE_FORMATION:    # 进入上阵界面时重置状态
            game.reset_formation()
        game.prev_state = game.game_state

    # 清屏
    screen.fill(BLACK)

    # 根据状态绘制不同界面
    if game.game_state == STATE_MENU:
        ui.draw_menu(screen)
    elif game.game_state == STATE_CHALLENGE:
        ui.draw_challenge(screen)
    elif game.game_state == STATE_CHALLENGE_BATTLE:
        ui.draw_battle(screen)
    elif game.game_state == STATE_UPGRADE:
        ui.draw_upgrade(screen)
    elif game.game_state == STATE_GACHA:
        ui.draw_gacha(screen)
    elif game.game_state == STATE_CONFIRM:
        ui.draw_confirm(screen)
    elif game.game_state == STATE_WORLD:
        ui.draw_world(screen)
    elif game.game_state == STATE_LOSE:
        ui.draw_lose(screen)
    elif game.game_state == STATE_WIN:
        ui.draw_win(screen)
    elif game.game_state == STATE_FORMATION:  
        ui.draw_formation(screen)
    elif game.game_state == STATE_MINING:
        ui.draw_mining(screen)

    # 更新屏幕
    pygame.display.flip()
    clock.tick(FPS)

# 游戏退出时自动保存一次
game.save_game()
print("游戏退出，已自动保存")

pygame.quit()
sys.exit()