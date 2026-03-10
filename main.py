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

            # 先让UI按钮处理
            if handlers.handle_ui_event(event):
                continue

            # 再处理非按钮点击
            if game.game_state == STATE_CHALLENGE_BATTLE:
                handlers.handle_battle_target_click(event.pos)
            # 其他特殊点击（如果有）...

        elif event.type == pygame.MOUSEWHEEL:     # 鼠标滚轮事件
            if game.game_state == STATE_UPGRADE:       # 仅在养成界面响应滚轮
                game.upgrade_scroll -= event.y
                visible_count = 6
                max_scroll = max(0, len(game.player_team) - visible_count)
                game.upgrade_scroll = max(0, min(game.upgrade_scroll, max_scroll))

    # ESC 返回上一级
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        if game.game_state == STATE_CHALLENGE:
            game.set_state(STATE_MENU)
        elif game.game_state == STATE_WORLD:
            game.set_state(STATE_MENU)

    # ===== 自动敌人攻击 =====
    if game.game_state == STATE_CHALLENGE_BATTLE and game.combatants and game.battle_sub_state == BATTLE_STATE_ACTION:
        current = game.combatants[game.current_index]
        if current["type"] == "enemy":
            # 敌人选择目标（随机选择存活的玩家）
            alive_players = [c for c in game.combatants if c["type"] == "player" and c["entity"]["hp"] > 0]
            if not alive_players:
                # 没有活着的玩家，直接失败
                game.set_state(STATE_LOSE)
            else:
                target = random.choice(alive_players)
                # 设置动画变量
                game.anim_attacker_idx = game.current_index
                game.anim_target_idx = game.combatants.index(target)
                game.anim_phase = 1
                game.anim_phase_frame = 0
                game.battle_sub_state = BATTLE_STATE_ANIM

    # ===== 动画处理 =====
    # （原来的 anim_offset 相关代码似乎未使用，保留但可能不需要）
    # 如果需要，可以类似修改，但这里省略

    # ===== 回合制战斗动画更新 =====
    if game.game_state == STATE_CHALLENGE_BATTLE and game.battle_sub_state == BATTLE_STATE_ANIM:
        game.anim_phase_frame += 1
        if game.anim_phase_frame >= ANIM_PHASE_FRAMES:
            game.anim_phase_frame = 0
            game.anim_phase += 1
            if game.anim_phase > 4:
                # 动画结束，执行实际攻击
                attacker_type = game.combatants[game.anim_attacker_idx]["type"]
                if attacker_type == "player":
                    result, next_index, new_skill_points = perform_attack(
                        game.combatants, game.anim_attacker_idx, game.anim_target_idx, game.current_skill_points)
                    game.current_skill_points = new_skill_points
                else:  # enemy
                    result, next_index = enemy_attack(game.combatants, game.anim_attacker_idx, game.anim_target_idx)

                if result == "win":
                    reward = get_reward_for_level(game.current_level)
                    game.win_reward = reward
                    game.add_reward(reward)
                    game.set_state(STATE_WIN)
                elif result == "lose":
                    game.set_state(STATE_LOSE)
                else:
                    game.current_index = next_index

                game.battle_sub_state = BATTLE_STATE_ACTION
                game.anim_phase = 0
                game.anim_attacker_idx = None
                game.anim_target_idx = None

    # ===== 检测状态变化并更新音乐 =====
    if game.game_state != game.prev_state:
        music.update_music(game.game_state)
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

    # 更新屏幕
    pygame.display.flip()
    clock.tick(FPS)

# 游戏退出时自动保存一次
game.save_game()
print("游戏退出，已自动保存")

pygame.quit()
sys.exit()