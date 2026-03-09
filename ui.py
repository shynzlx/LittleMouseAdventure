# ui.py - 所有绘制函数

import pygame
from constants import *
import avatar_mapper      # 初始化映射

CYAN = (0, 255, 255)

# 头像缓存
avatar_cache = {}

def load_avatar(role_name):
    """根据角色名称加载头像，返回缩放后的图片或 None"""
    filename = avatar_mapper.get_avatar_filename(role_name)
    if filename is None:
        return None  # 没有映射

    # 构建完整路径
    full_path = f"assets/avatars/{filename}"
    if full_path not in avatar_cache:
        try:
            img = pygame.image.load(full_path).convert_alpha()
            img = pygame.transform.scale(img, (180, 270))
            avatar_cache[full_path] = img
        except Exception as e:
            print(f"头像加载失败: {full_path} - {e}")
            avatar_cache[full_path] = None
    return avatar_cache[full_path]

def get_font(size, bold=False):
    font = pygame.font.Font(FONT_MEDIUM[0], size)
    if bold:
        font.set_bold(True)
    return font

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
    # 加载背景图片（从 assets 文件夹）
    try:
        bg_image = pygame.image.load('assets/main.png')
        # 缩放图片至窗口大小
        bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(bg_image, (0, 0))
    except:
        # 如果图片加载失败，就用纯黑色背景
        surface.fill(BLACK)
    # 计算按钮水平居中位置
    btn_x = (SCREEN_WIDTH - BTN_WIDTH) // 2
    # 按钮1：闯关模式（仅文字，无背景）
    draw_text(surface, "闯关模式", FONT_BIG[1], GREEN, btn_x + BTN_WIDTH//2, 250 + BTN_HEIGHT//2)
    # 按钮2：保存游戏
    draw_text(surface, "保存游戏", FONT_BIG[1], BLUE, btn_x + BTN_WIDTH//2, 400 + BTN_HEIGHT//2)
    # 按钮3：大世界（敬请期待）文字颜色用灰色
    draw_text(surface, "大世界（敬请期待）", FONT_BIG[1], (150,150,150), btn_x + BTN_WIDTH//2, 550 + BTN_HEIGHT//2)
    # 显示金币
    draw_text(surface, f"金币: {inventory.get('gold', 0)}", FONT_MEDIUM[1], BLACK, SCREEN_WIDTH - 220, 30)
    # 底部提示
    draw_text(surface, "点击按钮开始冒险！", FONT_MEDIUM[1], RED, SCREEN_WIDTH//2, 680)

    #右下角水平排列两个按钮
    margin = 20
    bottom_y = SCREEN_HEIGHT - MENU_BTN_HEIGHT - margin
    gacha_rect = pygame.Rect(SCREEN_WIDTH - MENU_BTN_WIDTH - margin, bottom_y, MENU_BTN_WIDTH, MENU_BTN_HEIGHT)
    draw_button(surface, gacha_rect, "抽卡", FONT_MEDIUM[1], ORANGE, YELLOW, WHITE)
    upgrade_rect = pygame.Rect(gacha_rect.left - MENU_BTN_WIDTH - margin, bottom_y, MENU_BTN_WIDTH, MENU_BTN_HEIGHT)
    draw_button(surface, upgrade_rect, "角色养成", FONT_MEDIUM[1], PURPLE, WHITE, WHITE)


# 绘制闯关模式
def draw_challenge(surface):
    draw_text(surface, "闯关模式", FONT_TITLE[1], GREEN, SCREEN_WIDTH//2, 120)
    draw_text(surface, "选择关卡", FONT_BIG[1], WHITE, SCREEN_WIDTH//2, 250)
    btn_x = (SCREEN_WIDTH - BTN_WIDTH) // 2
    draw_button(surface, pygame.Rect(btn_x - 100, 350, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT), "关卡1", FONT_MEDIUM[1], GRAY, GREEN, WHITE)
    draw_button(surface, pygame.Rect(btn_x + 150, 350, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT), "关卡2", FONT_MEDIUM[1], GRAY, GREEN, WHITE)
    draw_button(surface, pygame.Rect(btn_x + 400, 350, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT), "关卡3", FONT_MEDIUM[1], GRAY, GREEN, WHITE)
    # 返回主菜单按钮
    draw_button(surface, pygame.Rect(50, SCREEN_HEIGHT-100, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT), "返回主菜单", FONT_MEDIUM[1], GRAY, RED, WHITE)
    # 保留原有的ESC提示

# 绘制战斗界面（从 battle.py 调用）
# ui.py 中的 draw_battle 函数（替换成这个）

def draw_battle(surface, player_team, enemy, current_level, combatants, current_index, anim_offset=0):
    draw_text(surface, f"关卡 {current_level} - 战斗！", FONT_BIG[1], YELLOW, SCREEN_WIDTH//2, 50)

    # 队伍信息（左边）
    y = 150
    for role in player_team:
        # 在 combatants 中找到该角色对应的条目
        combatant = next((c for c in combatants if c["type"] == "player" and c["entity"] is role), None)
        remaining = combatant["remaining_time"] if combatant else 0

        # 判断是否当前行动者（用于高亮或动画）
        is_current = (combatant is not None and combatants[current_index] is combatant)

        # 角色名称
        name_color = GRAY if role["hp"] <= 0 else (YELLOW if is_current else WHITE)
        draw_text(surface, role["name"], FONT_MEDIUM[1], name_color, 150, y)

        # 血条
        draw_hp_bar(surface, 150, y+30, role["hp"], role["max_hp"])

        # HP数值
        hp_text = f"HP: {role['hp']}/{role['max_hp']}"
        draw_text(surface, hp_text, FONT_SMALL[1], name_color, 400, y+30)

        # 剩余时间条（可选）
        if remaining > 0:
            bar_width = 100
            fill_width = (remaining / BASE_TIME) * bar_width
            pygame.draw.rect(surface, GRAY, (400, y+50, bar_width, 5))
            pygame.draw.rect(surface, BLUE, (400, y+50, fill_width, 5))

        # 如果死亡，显示“无法行动”
        if role["hp"] <= 0:
            draw_text(surface, "无法行动", FONT_SMALL[1], RED, 520, y+30)

        # 如果是当前行动者且 anim_offset != 0，绘制偏移效果（模拟攻击前移）
        if is_current and anim_offset != 0:
            # 临时在角色位置绘制一个影子或直接移动文本？简单起见，我们移动名字
            draw_text(surface, role["name"], FONT_MEDIUM[1], name_color, 150 + anim_offset, y)

        y += 80

    # 敌人信息
    enemy_combatant = combatants[-1] if combatants and combatants[-1]["type"] == "enemy" else None
    enemy_remaining = enemy_combatant["remaining_time"] if enemy_combatant else 0
    is_enemy_current = (enemy_combatant is not None and combatants[current_index] is enemy_combatant)

    enemy_name_color = YELLOW if is_enemy_current else RED
    draw_text(surface, enemy["name"], FONT_BIG[1], enemy_name_color, SCREEN_WIDTH//2 +200, 200)
    draw_hp_bar(surface, SCREEN_WIDTH//2 +100, 250, enemy["hp"], enemy["max_hp"], color=RED)
    draw_text(surface, f"HP: {enemy['hp']}/{enemy['max_hp']}", FONT_MEDIUM[1], WHITE, SCREEN_WIDTH//2 +200, 280)

    # 敌人剩余时间条
    if enemy_remaining > 0:
        bar_width = 100
        fill_width = (enemy_remaining / BASE_TIME) * bar_width
        pygame.draw.rect(surface, GRAY, (SCREEN_WIDTH//2 +100, 300, bar_width, 5))
        pygame.draw.rect(surface, RED, (SCREEN_WIDTH//2 +100, 300, fill_width, 5))

    # 战斗按钮（仅在轮到玩家时可用，但这里不处理逻辑，仅绘制）
    # 如果当前行动者是玩家，按钮正常颜色；否则变灰
    current_is_player = (combatants[current_index]["type"] == "player") if combatants else False
    if current_is_player:
        btn_attack_color = BLUE
        btn_skill_color = PURPLE
    else:
        btn_attack_color = GRAY
        btn_skill_color = GRAY

    draw_button(surface, pygame.Rect(100, 500, 150, 60), "攻击", FONT_MEDIUM[1], GRAY, btn_attack_color, WHITE)
    draw_button(surface, pygame.Rect(300, 500, 150, 60), "技能(治疗)", FONT_MEDIUM[1], GRAY, btn_skill_color, WHITE)
    draw_button(surface, pygame.Rect(500, 500, 150, 60), "逃跑", FONT_MEDIUM[1], GRAY, GRAY, WHITE)

# 绘制养成界面（从 upgrade.py 调用）
def draw_upgrade(surface, player_team, selected_role_index, inventory, scroll):
    draw_text(surface, "角色养成", FONT_TITLE[1], YELLOW, SCREEN_WIDTH//2, 60)

    # 计算可见角色范围
    visible_count = 6  # 一次最多显示6个
    start_idx = scroll
    end_idx = min(start_idx + visible_count, len(player_team))
    visible_roles = player_team[start_idx:end_idx]

    # 绘制角色列表（左侧）
    y = 150
    for i, role in enumerate(visible_roles):
        actual_idx = start_idx + i  # 实际在 player_team 中的索引
        # 按钮背景色：选中时用角色颜色，否则灰色
        color = role["color"] if actual_idx == selected_role_index else GRAY
        # 按钮边框：如果角色上阵，边框用金色，否则白色
        border_color = YELLOW if role.get("active", False) else WHITE
        # 绘制角色按钮
        button_rect = pygame.Rect(50, y, 200, 80)
        draw_button(surface, button_rect, role["name"], FONT_MEDIUM[1], color, border_color, WHITE)
        y += 100

    # 绘制滚动提示（如果有多页）
    if len(player_team) > visible_count:
        draw_text(surface, f"↑ 滚动查看 ({start_idx+1}-{end_idx}/{len(player_team)})", FONT_SMALL[1], RED, 150, 550)

    # 详细信息（右侧）
    if player_team:
        role = player_team[selected_role_index]
        # 尝试加载头像
        avatar_img = load_avatar(role["name"])
        if avatar_img:
           surface.blit(avatar_img, (300, 150))
        else:
        # 如果没有头像，画纯色占位（改为正方形，与头像尺寸一致）
            pygame.draw.rect(surface, role["color"], (300, 150, 180, 270))
        draw_text(surface, role["name"], FONT_BIG[1], WHITE, 390, 120)
        y = 180
        draw_text(surface, f"稀有度: {role['rarity']}", FONT_MEDIUM[1], ORANGE, 650, y); y += 40
        draw_text(surface, f"等级: Lv.{role['level']}", FONT_MEDIUM[1], YELLOW, 650, y); y += 40
        draw_text(surface, f"经验: {role['exp']}/{role['exp_to_next']}", FONT_MEDIUM[1], WHITE, 650, y); y += 40
        draw_text(surface, f"HP: {role['hp']}/{role['max_hp']}", FONT_MEDIUM[1], GREEN, 650, y); y += 40
        draw_text(surface, f"攻击: {role['atk']}", FONT_MEDIUM[1], RED, 650, y); y += 40
        draw_text(surface, f"耐力: {role['stamina']}", FONT_MEDIUM[1], BLUE, 650, y); y += 40
        draw_text(surface, f"速度: {role['speed']}", FONT_MEDIUM[1], CYAN, 650, y); y += 40
        draw_text(surface, "技能：", FONT_MEDIUM[1], WHITE, 400, 480)
        sy = 520
        for sk in role["skills"]:
            draw_text(surface, f"{sk['name']} Lv.{sk['level']} ({sk['proficiency']}/{sk['prof_to_next']})", FONT_SMALL[1], WHITE, 320, sy)
            sy += 35

        # 切换按钮（根据当前状态显示不同文字）
        btn_x = 600
        btn_y = 550  # 调整位置避免与道具按钮重叠
        btn_rect = pygame.Rect(btn_x, btn_y, 180, 60)
        if role.get("active", False):
            draw_button(surface, btn_rect, "设为待命", FONT_MEDIUM[1], GRAY, RED, WHITE)
        else:
            draw_button(surface, btn_rect, "设为上阵", FONT_MEDIUM[1], GRAY, GREEN, WHITE)

    # 道具按钮（调整位置）
    draw_button(surface, pygame.Rect(600, 450, 180, 60), f"经验书 ({inventory['exp_book']})", FONT_MEDIUM[1], GRAY, GREEN, WHITE)
    draw_button(surface, pygame.Rect(800, 450, 180, 60), f"技能书 ({inventory['skill_book']})", FONT_MEDIUM[1], GRAY, PURPLE, WHITE)
    #返回
    draw_button(surface, pygame.Rect(50, SCREEN_HEIGHT-100, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT), "返回主菜单", FONT_MEDIUM[1], GRAY, RED, WHITE)

# 绘制抽卡界面
def draw_gacha(surface, gacha_result=None):
    draw_text(surface, "抽卡系统", FONT_TITLE[1], ORANGE, SCREEN_WIDTH//2, 120)
    # 抽卡按钮
    draw_button(surface, pygame.Rect((SCREEN_WIDTH-BTN_WIDTH)//2, 350, BTN_WIDTH, BTN_HEIGHT), "抽卡一次", FONT_BIG[1], GRAY, YELLOW, WHITE)
    if gacha_result:
        draw_text(surface, f"抽到 {gacha_result['rarity']} 角色: {gacha_result['name']}", FONT_BIG[1], gacha_result["color"], SCREEN_WIDTH//2, 500)
    # 返回按钮（左下角）
    draw_button(surface, pygame.Rect(50, SCREEN_HEIGHT-100, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT), "返回主菜单", FONT_MEDIUM[1], GRAY, RED, WHITE)

#绘制关卡确认对话框
def draw_confirm(surface, level):
    # 半透明遮罩
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    surface.blit(overlay, (0, 0))
    # 对话框背景
    dialog_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 100, 400, 200)
    pygame.draw.rect(surface, DARK_GRAY, dialog_rect, border_radius=10)
    pygame.draw.rect(surface, WHITE, dialog_rect, 3, border_radius=10)
    # 文字
    draw_text(surface, f"确定要进入关卡 {level} 吗？", FONT_MEDIUM[1], WHITE, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40)
    # 两个按钮
    btn_w, btn_h = 120, 50
    btn_y = SCREEN_HEIGHT//2 + 20
    # 返回按钮
    return_rect = pygame.Rect(SCREEN_WIDTH//2 - 140, btn_y, btn_w, btn_h)
    draw_button(surface, return_rect, "返回", FONT_MEDIUM[1], GRAY, RED, WHITE)
    # 冲鸭按钮
    go_rect = pygame.Rect(SCREEN_WIDTH//2 + 20, btn_y, btn_w, btn_h)
    draw_button(surface, go_rect, "出发！", FONT_MEDIUM[1], GRAY, GREEN, WHITE)

#绘制失败提示画面
def draw_lose(surface):
    # 半透明遮罩
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    surface.blit(overlay, (0, 0))
    # 对话框背景
    dialog_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 100, 400, 200)
    pygame.draw.rect(surface, DARK_GRAY, dialog_rect, border_radius=10)
    pygame.draw.rect(surface, WHITE, dialog_rect, 3, border_radius=10)
    # 文字
    draw_text(surface, "你失败了！", FONT_BIG[1], RED, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40)
    # 确认按钮
    btn_w, btn_h = 120, 50
    btn_rect = pygame.Rect(SCREEN_WIDTH//2 - btn_w//2, SCREEN_HEIGHT//2 + 20, btn_w, btn_h)
    draw_button(surface, btn_rect, "确认", FONT_MEDIUM[1], GRAY, GREEN, WHITE)

#绘制胜利界面
def draw_win(surface, reward):
    # 半透明遮罩
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    surface.blit(overlay, (0, 0))
    # 对话框背景
    dialog_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 100, 400, 200)
    pygame.draw.rect(surface, DARK_GRAY, dialog_rect, border_radius=10)
    pygame.draw.rect(surface, WHITE, dialog_rect, 3, border_radius=10)
    
    # 标题
    draw_text(surface, "战斗胜利！", FONT_BIG[1], YELLOW, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40)
    
    # 显示奖励（如果有）
    if reward:
        y = SCREEN_HEIGHT//2
        draw_text(surface, f"获得金币: {reward.get('gold', 0)}", FONT_MEDIUM[1], YELLOW, SCREEN_WIDTH//2, y)
        y += 40
        draw_text(surface, f"获得经验书: {reward.get('exp_book', 0)}", FONT_MEDIUM[1], YELLOW, SCREEN_WIDTH//2, y)
        y += 40
        draw_text(surface, f"获得技能书: {reward.get('skill_book', 0)}", FONT_MEDIUM[1], YELLOW, SCREEN_WIDTH//2, y)
    
    # 确认按钮
    btn_w, btn_h = 120, 50
    btn_rect = pygame.Rect(SCREEN_WIDTH//2 - btn_w//2, SCREEN_HEIGHT//2 + 20, btn_w, btn_h)
    draw_button(surface, btn_rect, "确认", FONT_MEDIUM[1], GRAY, GREEN, WHITE)