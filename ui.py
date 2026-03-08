# ui.py - 所有绘制函数

import pygame
from constants import *

def get_font(size, bold=False):
    return pygame.font.SysFont(FONT_MEDIUM[0], size, bold)

def draw_text(surface, text, font_size, color, x, y, center=True):
    font = get_font(font_size)
    text_surf = font.render(text, True, color)
    rect = text_surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(text_surf, rect)

def draw_button(surface, rect, text, font_size, bg_color, border_color, text_color):
    pygame.draw.rect(surface, bg_color, rect, border_radius=15)
    pygame.draw.rect(surface, border_color, rect, 5, border_radius=15)
    draw_text(surface, text, font_size, text_color, rect.centerx, rect.centery)

def draw_hp_bar(surface, x, y, current, max_val, width=200, height=20, color=RED):
    bar_rect = pygame.Rect(x, y, width, height)
    fill_width = (current / max_val) * width if max_val > 0 else 0
    pygame.draw.rect(surface, GRAY, bar_rect)
    pygame.draw.rect(surface, color, (x, y, fill_width, height))


# 绘制主菜单
def draw_menu(surface, inventory):
    draw_text(surface, "冒险游戏", FONT_TITLE[1], WHITE, SCREEN_WIDTH//2, 150)
    
    btn_x = (SCREEN_WIDTH - BTN_WIDTH) // 2
    
    draw_button(surface, pygame.Rect(btn_x, 250, BTN_WIDTH, BTN_HEIGHT), "闯关模式", FONT_BIG[1], GRAY, GREEN, WHITE)
    draw_button(surface, pygame.Rect(btn_x, 400, BTN_WIDTH, BTN_HEIGHT), "保存游戏", FONT_BIG[1], GRAY, BLUE, WHITE)  # ← 新增保存按钮
    draw_button(surface, pygame.Rect(btn_x, 550, BTN_WIDTH, BTN_HEIGHT), "大世界（敬请期待）", FONT_BIG[1], DARK_GRAY, GRAY, (150,150,150))
    
    # 显示金币
    draw_text(surface, f"金币: {inventory.get('gold', 0)}", FONT_MEDIUM[1], YELLOW, SCREEN_WIDTH - 220, 30)
    
    draw_text(surface, "点击按钮开始冒险！", FONT_MEDIUM[1], WHITE, SCREEN_WIDTH//2, 680)


# 绘制闯关模式
def draw_challenge(surface):
    draw_text(surface, "闯关模式", FONT_TITLE[1], GREEN, SCREEN_WIDTH//2, 120)
    draw_text(surface, "选择关卡", FONT_BIG[1], WHITE, SCREEN_WIDTH//2, 250)
    btn_x = (SCREEN_WIDTH - BTN_WIDTH) // 2
    draw_button(surface, pygame.Rect(btn_x - 100, 350, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT), "关卡1", FONT_MEDIUM[1], GRAY, GREEN, WHITE)
    draw_button(surface, pygame.Rect(btn_x + 150, 350, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT), "关卡2", FONT_MEDIUM[1], GRAY, GREEN, WHITE)
    draw_button(surface, pygame.Rect(btn_x + 400, 350, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT), "关卡3", FONT_MEDIUM[1], GRAY, GREEN, WHITE)
    draw_button(surface, pygame.Rect(btn_x, 500, BTN_WIDTH, BTN_SMALL_HEIGHT), "角色养成", FONT_MEDIUM[1], PURPLE, WHITE, WHITE)
    draw_button(surface, pygame.Rect(btn_x, 600, BTN_WIDTH, BTN_SMALL_HEIGHT), "抽卡", FONT_MEDIUM[1], ORANGE, YELLOW, WHITE)  # 新增抽卡按钮
    draw_text(surface, "ESC 返回主菜单", FONT_SMALL[1], GRAY, 50, SCREEN_HEIGHT-50)

# 绘制战斗界面（从 battle.py 调用）
# ui.py 中的 draw_battle 函数（替换成这个）

def draw_battle(surface, player_team, enemy, current_level):
    draw_text(surface, f"关卡 {current_level} - 战斗！", FONT_BIG[1], YELLOW, SCREEN_WIDTH//2, 50)

    # 队伍信息（左边）
    y = 150
    for role in player_team:
        draw_text(surface, role["name"], FONT_MEDIUM[1], WHITE, 150, y)
        draw_hp_bar(surface, 150, y+30, role["hp"], role["max_hp"])
        draw_text(surface, f"HP: {role['hp']}/{role['max_hp']}", FONT_SMALL[1], WHITE, 400, y+30)
        y += 80
    # 敌人（中间偏右）
    draw_text(surface, enemy["name"], FONT_BIG[1], RED, SCREEN_WIDTH//2 +200, 200)
    draw_hp_bar(surface, SCREEN_WIDTH//2 +100, 250, enemy["hp"], enemy["max_hp"], color=RED)
    draw_text(surface, f"HP: {enemy['hp']}/{enemy['max_hp']}", FONT_MEDIUM[1], WHITE, SCREEN_WIDTH//2 +200, 280)
    # 战斗按钮（底部）
    draw_button(surface, pygame.Rect(100, 500, 150, 60), "攻击", FONT_MEDIUM[1], GRAY, BLUE, WHITE)
    draw_button(surface, pygame.Rect(300, 500, 150, 60), "技能(治疗)", FONT_MEDIUM[1], GRAY, PURPLE, WHITE)
    draw_button(surface, pygame.Rect(500, 500, 150, 60), "逃跑", FONT_MEDIUM[1], GRAY, GRAY, WHITE)

    draw_text(surface, "ESC 返回选关", FONT_SMALL[1], GRAY, 50, SCREEN_HEIGHT-50)

# 绘制养成界面（从 upgrade.py 调用）
def draw_upgrade(surface, player_team, selected_role_index, inventory):
    draw_text(surface, "角色养成", FONT_TITLE[1], YELLOW, SCREEN_WIDTH//2, 60)
    # 角色列表
    for i, role in enumerate(player_team):
        color = role["color"] if i == selected_role_index else GRAY
        draw_button(surface, pygame.Rect(50, 150 + i*100, 200, 80), role["name"], FONT_MEDIUM[1], color, WHITE, WHITE)
    # 详细信息
    if player_team:
        role = player_team[selected_role_index]
        pygame.draw.rect(surface, role["color"], (300, 150, 180, 300))  # 全身像占位
        draw_text(surface, role["name"], FONT_BIG[1], WHITE, 390, 120)
        y = 180
        draw_text(surface, f"稀有度: {role['rarity']}", FONT_MEDIUM[1], ORANGE, 520, y); y += 40
        draw_text(surface, f"等级: Lv.{role['level']}", FONT_MEDIUM[1], YELLOW, 520, y); y += 40
        draw_text(surface, f"经验: {role['exp']}/{role['exp_to_next']}", FONT_MEDIUM[1], WHITE, 520, y); y += 40
        draw_text(surface, f"HP: {role['hp']}/{role['max_hp']}", FONT_MEDIUM[1], GREEN, 520, y); y += 40
        draw_text(surface, f"攻击: {role['atk']}", FONT_MEDIUM[1], RED, 520, y); y += 40
        draw_text(surface, f"耐力: {role['stamina']}", FONT_MEDIUM[1], BLUE, 520, y); y += 40
        draw_text(surface, "技能：", FONT_MEDIUM[1], WHITE, 300, 480)
        sy = 520
        for sk in role["skills"]:
            draw_text(surface, f"{sk['name']} Lv.{sk['level']} ({sk['proficiency']}/{sk['prof_to_next']})", FONT_SMALL[1], WHITE, 320, sy)
            sy += 35
    # 按钮
    draw_button(surface, pygame.Rect(600, 500, 180, 60), f"经验书 ({inventory['exp_book']})", FONT_MEDIUM[1], GRAY, GREEN, WHITE)
    draw_button(surface, pygame.Rect(800, 500, 180, 60), f"技能书 ({inventory['skill_book']})", FONT_MEDIUM[1], GRAY, PURPLE, WHITE)
    draw_text(surface, "ESC 返回选关", FONT_SMALL[1], GRAY, 50, SCREEN_HEIGHT-50)

# 绘制抽卡界面（从 gacha.py 调用）
def draw_gacha(surface, gacha_result=None):
    draw_text(surface, "抽卡系统", FONT_TITLE[1], ORANGE, SCREEN_WIDTH//2, 120)
    draw_button(surface, pygame.Rect((SCREEN_WIDTH-BTN_WIDTH)//2, 350, BTN_WIDTH, BTN_HEIGHT), "抽卡一次", FONT_BIG[1], GRAY, YELLOW, WHITE)
    if gacha_result:
        draw_text(surface, f"抽到 {gacha_result['rarity']} 角色: {gacha_result['name']}", FONT_BIG[1], gacha_result["color"], SCREEN_WIDTH//2, 500)
    draw_text(surface, "ESC 返回选关", FONT_SMALL[1], GRAY, 50, SCREEN_HEIGHT-50)