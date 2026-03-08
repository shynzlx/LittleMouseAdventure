# main.py - 游戏主入口和主循环

import pygame
import sys

# 导入所有模块（确保这些文件都在同一目录）
from constants import *
from ui import *
from handlers import *
from battle import *
from upgrade import *
from gacha import *
from levels import *
from save import *

# 初始化 Pygame
pygame.init()

# 创建窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("冒险游戏")

# 时钟控制帧率
clock = pygame.time.Clock()

# 游戏状态和全局变量
game_state = STATE_MENU
battle_turn = "player"           # "player" 或 "enemy"
current_level = 1
enemy = {}                       # 当前敌人
selected_role_index = 0          # 养成界面选中的角色
gacha_result = None              # 抽卡结果临时显示

# 加载存档（启动时自动执行）
player_team, inventory, current_level = load_game()

# 如果加载失败或队伍为空，给默认初始战士
if not player_team:
    player_team = [
        {
            "name": "一般鼠鼠",
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
    inventory = {"gold": 1000, "exp_book": 0, "skill_book": 0}
    current_level = 1
    print("使用默认初始数据（新玩家）")

# 主循环
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == STATE_MENU:
                result = handle_menu_click(mouse_pos, game_state)
                if result == "save":
                    save_game(player_team, inventory, current_level)
                    print("手动保存成功！")
                else:
                    game_state = result
            
            elif game_state == STATE_CHALLENGE:
                new_state, new_level = handle_challenge_click(mouse_pos, game_state, current_level, player_team)
                if new_state == STATE_CHALLENGE_BATTLE:
                    enemy = setup_enemy(new_level)  # 设置敌人数据
                game_state = new_state
                current_level = new_level
            
            elif game_state == STATE_CHALLENGE_BATTLE:
                # 处理玩家点击（攻击、技能、逃跑）
                game_state, battle_turn = handle_battle_click(mouse_pos, game_state, player_team, enemy, battle_turn)
                # 敌人回合
                if battle_turn == "enemy":
                    game_state, battle_turn = enemy_attack(player_team, enemy, game_state, battle_turn)
            
            elif game_state == STATE_UPGRADE:
                selected_role_index = handle_upgrade_click(mouse_pos, selected_role_index, player_team, inventory)
            
            elif game_state == STATE_GACHA:
                result = handle_gacha_click(mouse_pos, player_team, inventory)
                if result:
                    gacha_result = result  # 保存最新抽到的角色用于显示

    # ESC 返回上一级
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        if game_state in (STATE_CHALLENGE_BATTLE, STATE_UPGRADE, STATE_GACHA):
            game_state = STATE_CHALLENGE
        elif game_state == STATE_CHALLENGE:
            game_state = STATE_MENU
        elif game_state == STATE_WORLD:
            game_state = STATE_MENU

    # 清屏
    screen.fill(BLACK)

    # 根据状态绘制不同界面
    if game_state == STATE_MENU:
        draw_menu(screen, inventory)
    
    elif game_state == STATE_CHALLENGE:
        draw_challenge(screen)
    
    elif game_state == STATE_CHALLENGE_BATTLE:
        draw_battle(screen, player_team, enemy, current_level)
        # 敌人回合（如果轮到敌人）
        if battle_turn == "enemy":
            game_state, battle_turn = enemy_attack(player_team, enemy, game_state, battle_turn)
    
    elif game_state == STATE_UPGRADE:
        draw_upgrade(screen, player_team, selected_role_index, inventory)
    
    elif game_state == STATE_GACHA:
        draw_gacha(screen, gacha_result)
        # 在抽卡界面右上角显示金币
        draw_text(screen, f"金币: {inventory.get('gold', 0)}", FONT_MEDIUM[1], YELLOW, SCREEN_WIDTH - 150, 50)
    
    elif game_state == STATE_WORLD:
        draw_text(screen, "大世界模式", FONT_TITLE[1], BLUE, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50)
        draw_text(screen, "（开发中，按 ESC 返回）", FONT_MEDIUM[1], WHITE, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)

    # 更新屏幕
    pygame.display.flip()
    clock.tick(FPS)

# 游戏退出时自动保存一次
save_game(player_team, inventory, current_level)
print("游戏退出，已自动保存")

pygame.quit()
sys.exit()