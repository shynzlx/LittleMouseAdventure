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
upgrade_scroll = 0               # 养成界面的滚动偏移量
confirm_level = 1                # 待确认的关卡

# 辅助函数：获取当前上阵角色
def get_active_team(team):
    return [r for r in team if r.get("active", False)]

# 加载存档（启动时自动执行）
player_team, inventory, current_level = load_game()

# 如果加载失败或队伍为空，给默认初始鼠鼠
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

# 为所有角色添加 active 字段（如果没有）
for i, role in enumerate(player_team):
    if "active" not in role:
        role["active"] = (i < 5)  # 前5个默认上阵


# 主循环
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    # 处理事件
    # 事件处理循环
    for event in pygame.event.get():
        if event.type == pygame.QUIT:          # 关闭窗口事件
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:   # 鼠标按键按下（左键）
            if event.button in (4, 5):
                continue
            
            # 根据当前游戏状态处理点击事件
            if game_state == STATE_MENU:        # 主菜单
                result = handle_menu_click(mouse_pos, game_state)
                if result == "save":            # 保存按钮
                    save_game(player_team, inventory, current_level)
                    print("手动保存成功！")
                else:                            # 其他按钮（闯关、大世界）
                    game_state = result
            
            elif game_state == STATE_CHALLENGE:  # 闯关模式（选关界面）
                new_state, new_level = handle_challenge_click(mouse_pos, game_state, current_level, player_team)
                if new_state == STATE_CONFIRM:
                    confirm_level = new_level
                    game_state = STATE_CONFIRM
                else:
                    game_state = new_state
                    current_level = new_level
            
            elif game_state == STATE_CHALLENGE_BATTLE:  # 战斗界面
                active_team = get_active_team(player_team)        # 仅使用上阵角色
                # 处理玩家点击（攻击、技能、逃跑）
                game_state, battle_turn = handle_battle_click(mouse_pos, game_state, active_team, enemy, battle_turn)
                # 如果轮到敌人，立即执行敌人攻击（并更新状态）
                if battle_turn == "enemy":
                    game_state, battle_turn = enemy_attack(active_team, enemy, game_state, battle_turn)
            
            elif game_state == STATE_UPGRADE:   # 养成界面
                new_state, selected_role_index = handle_upgrade_click(mouse_pos, selected_role_index, player_team, inventory, upgrade_scroll)
                game_state = new_state
            
            elif game_state == STATE_GACHA:
                result = handle_gacha_click(mouse_pos, player_team, inventory)
                if result == "back":                     # 点击了返回按钮
                    game_state = STATE_CHALLENGE
                elif result:                              # 抽到新角色
                    gacha_result = result
            
            elif game_state == STATE_CONFIRM:  #选关确认界面
                result = handle_confirm_click(mouse_pos, confirm_level)
                if result:
                    action, lvl = result
                    if action == 'go':
                        active_team = get_active_team(player_team)
                        if not active_team:
                            print("没有上阵角色，无法战斗！")
                            game_state = STATE_CHALLENGE
                        else:
                            enemy = setup_enemy(lvl)
                            current_level = lvl
                            game_state = STATE_CHALLENGE_BATTLE
                    elif action == 'back':
                        game_state = STATE_CHALLENGE
        
        elif event.type == pygame.MOUSEWHEEL:     # 鼠标滚轮事件
            if game_state == STATE_UPGRADE:       # 仅在养成界面响应滚轮
                # event.y: 向上滚动为负，向下为正
                upgrade_scroll -= event.y
                visible_count = 6                  # 养成界面一次显示6个角色
                max_scroll = max(0, len(player_team) - visible_count)   # 最大滚动偏移
                upgrade_scroll = max(0, min(upgrade_scroll, max_scroll)) # 限制在有效范围内

    # ESC 返回上一级
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        if game_state == STATE_CHALLENGE:
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
        active_team = get_active_team(player_team)
        draw_battle(screen, active_team, enemy, current_level)
    
    elif game_state == STATE_UPGRADE:
        draw_upgrade(screen, player_team, selected_role_index, inventory, upgrade_scroll)
    
    elif game_state == STATE_GACHA:
        draw_gacha(screen, gacha_result)
        # 在抽卡界面右上角显示金币
        draw_text(screen, f"金币: {inventory.get('gold', 0)}", FONT_MEDIUM[1], YELLOW, SCREEN_WIDTH - 150, 50)
    
    elif game_state == STATE_CONFIRM:
        draw_confirm(screen, confirm_level)
    
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
