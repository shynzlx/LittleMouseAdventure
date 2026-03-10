# ui.py - 所有绘制函数

import pygame
from constants import *
import avatar_mapper      # 初始化映射
import formation

CYAN = (0, 255, 255)

# 头像缓存
avatar_cache = {}

# ui.py

def load_avatar(role_name, size=(180, 270)):
    """根据角色名称加载头像，返回指定尺寸的图片或 None"""
    filename = avatar_mapper.get_avatar_filename(role_name)
    if filename is None:
        return None

    full_path = f"assets/avatars/{filename}"
    cache_key = f"{full_path}_{size[0]}_{size[1]}"   # 包含尺寸的缓存键
    if cache_key not in avatar_cache:
        try:
            img = pygame.image.load(full_path).convert_alpha()
            img = pygame.transform.scale(img, size)
            avatar_cache[cache_key] = img
        except Exception as e:
            print(f"头像加载失败: {full_path} - {e}")
            avatar_cache[cache_key] = None
    return avatar_cache[cache_key]

def load_attack_avatar(role_name, size=(180, 270)):
    """根据角色名称加载进攻头像，返回指定尺寸的图片或 None"""
    filename = avatar_mapper.get_attack_avatar_filename(role_name)
    if filename is None:
        return None

    full_path = f"assets/avatars/{filename}"
    cache_key = f"{full_path}_{size[0]}_{size[1]}"
    if cache_key not in avatar_cache:
        try:
            img = pygame.image.load(full_path).convert_alpha()
            img = pygame.transform.scale(img, size)
            avatar_cache[cache_key] = img
        except Exception as e:
            print(f"进攻头像加载失败: {full_path} - {e}")
            avatar_cache[cache_key] = None
    return avatar_cache[cache_key]

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

def draw_turn_order(surface, combatants, current_index, x, y, width=150, entry_height=30):
    """
    绘制攻击顺序列表
    :param surface: pygame 表面
    :param combatants: 战斗单位列表
    :param current_index: 当前行动单位在 combatants 中的索引
    :param x: 列表左上角 x 坐标
    :param y: 列表左上角 y 坐标
    :param width: 列表宽度
    :param entry_height: 每个条目高度
    """
    draw_turn_order_x = x - 20
    draw_turn_order_y = y - 70
    draw_turn_order_width = width - 20

    if not combatants:  # 如果没有战斗单位，直接返回
        return

    # 按剩余时间从小到大排序（时间越短越快行动）
    sorted_combatants = sorted(combatants, key=lambda c: c["remaining_time"])

    # 绘制半透明背景
    bg_height = len(sorted_combatants) * entry_height + 100
    bg_surf = pygame.Surface((draw_turn_order_width, bg_height))
    bg_surf.set_alpha(90)
    bg_surf.fill(WHITE)
    surface.blit(bg_surf, (draw_turn_order_x, draw_turn_order_y - 20))

    # 绘制标题
    draw_text(surface, "攻击顺序", 20, WHITE, draw_turn_order_x + draw_turn_order_width // 2, draw_turn_order_y)

    # 绘制每个单位
    for i, c in enumerate(sorted_combatants):
        current_y = y + i * entry_height
        entity = c["entity"]
        name = entity.get("name", "未知")

        # 判断颜色
        if c == combatants[current_index]:
            color = YELLOW          # 当前行动者高亮
        elif c["type"] == "player":
            # 玩家单位：存活为绿色，死亡为灰色
            color = GREEN if entity["hp"] > 0 else GRAY
        else:
            # 敌人单位：存活为红色，死亡为灰色
            color = RED if entity["hp"] > 0 else GRAY
        # 绘制名称（居中）
        draw_text(surface, name, 20, color, draw_turn_order_x + draw_turn_order_width // 2, current_y)

# ui.py - 重写 draw_battle 函数

import formation

def draw_battle(surface, player_team, enemies, current_level, combatants, current_index,
                anim_offset, skill_points, battle_sub_state, anim_attacker_idx, anim_target_idx, anim_phase, anim_phase_frame):
    draw_text(surface, f"关卡 {current_level} - 战斗！", FONT_BIG[1], YELLOW, SCREEN_WIDTH//2, 50)
    draw_text(surface, f"技能点: {skill_points}", FONT_MEDIUM[1], CYAN, SCREEN_WIDTH - 150, 100)
    draw_turn_order(surface, combatants, current_index, x=20, y=150)

    # 提示当前状态
    if battle_sub_state == BATTLE_STATE_TARGET:
        draw_text(surface, "请选择攻击目标", FONT_SMALL[1], YELLOW, SCREEN_WIDTH//2, 120)

    # 构建实体到屏幕位置的映射（使用 id 作为键）
    entity_pos = {}
    player_slots = formation.get_player_slots(player_team)
    for role, idx, pos in player_slots:
        if role is not None:
            entity_pos[id(role)] = pos
    enemy_slots = formation.get_enemy_slots(enemies)
    for enemy, idx, pos in enemy_slots:
        if enemy is not None:
            entity_pos[id(enemy)] = pos

    # 玩家站位绘制
    for role, slot_idx, pos in player_slots:
        if role is None:
            pygame.draw.rect(surface, GRAY, (*pos, formation.SLOT_WIDTH, formation.SLOT_HEIGHT), 2)
            continue

        # 找出该角色在combatants中的信息
        combatant = next((c for c in combatants if c["type"] == "player" and c["entity"] is role), None)
        is_current = (combatant is not None and combatants[current_index] is combatant)

        # 判断是否正在动画中且是该角色（攻击者）
        anim_active = (battle_sub_state == BATTLE_STATE_ANIM and 
                       anim_attacker_idx is not None and 
                       combatants[anim_attacker_idx]["entity"] is role)

        # 计算攻击者移动偏移（真正移动到目标位置）
        offset_x = 0
        offset_y = 0
        if anim_active and anim_target_idx is not None:
            target_entity = combatants[anim_target_idx]["entity"]
            start_pos = pos
            target_pos = entity_pos.get(id(target_entity))
            if target_pos:
                move_vector = (target_pos[0] - start_pos[0] - 140, target_pos[1] - start_pos[1])
                if anim_phase == 1:      # 前移
                    progress = anim_phase_frame / ANIM_PHASE_FRAMES
                    offset_x = move_vector[0] * progress
                    offset_y = move_vector[1] * progress
                elif anim_phase == 2:    # 攻击图片，保持在目标面前
                    offset_x = move_vector[0]
                    offset_y = move_vector[1]
                elif anim_phase == 3:    # 后移
                    progress = 1 - (anim_phase_frame / ANIM_PHASE_FRAMES)
                    offset_x = move_vector[0] * progress
                    offset_y = move_vector[1] * progress

        # 选择头像（攻击阶段使用进攻图片）
        if anim_active and anim_phase == 2:
            img = load_attack_avatar(role["name"], size=(80, 120))
        else:
            img = load_avatar(role["name"], size=(80, 120))

        draw_pos = (pos[0] + offset_x, pos[1] + offset_y)
        if img:
            surface.blit(img, draw_pos)
        else:
            pygame.draw.rect(surface, role["color"], (*draw_pos, 80, 120))

        # 绘制名称和HP（保持在原位置，不随角色移动）
        name_color = GRAY if role["hp"] <= 0 else (YELLOW if is_current else WHITE)
        draw_text(surface, role["name"], FONT_SMALL[1], name_color, pos[0] + formation.SLOT_WIDTH * 2, pos[1] + formation.SLOT_HEIGHT//2 - 20)
        hp_display = max(0, role["hp"])
        hp_text = f"HP: {hp_display}/{role['max_hp']}"
        draw_text(surface, hp_text, FONT_SMALL[1], name_color, pos[0] + formation.SLOT_WIDTH * 2, pos[1] + formation.SLOT_HEIGHT//2 + 20)

        if role["hp"] <= 0:
            s = pygame.Surface((formation.SLOT_WIDTH, formation.SLOT_HEIGHT))
            s.set_alpha(128)
            s.fill(GRAY)
            surface.blit(s, pos)

    # 敌人站位绘制
    for enemy, idx, pos in enemy_slots:
        if enemy is None:
            pygame.draw.rect(surface, GRAY, (*pos, formation.SLOT_WIDTH, formation.SLOT_HEIGHT), 2)
            continue

        # 找出该敌人在 combatants 中的信息
        combatant = next((c for c in combatants if c["type"] == "enemy" and c["entity"] is enemy), None)
        is_current = (combatant is not None and combatants[current_index] is combatant)

        # 判断是否正在动画中且是该敌人（作为攻击者）
        anim_active = (battle_sub_state == BATTLE_STATE_ANIM and
                       anim_attacker_idx is not None and
                       combatants[anim_attacker_idx]["entity"] is enemy)

        # 计算攻击者的移动偏移（与玩家完全相同）
        offset_x, offset_y = 0, 0
        if anim_active and anim_target_idx is not None:
            target_entity = combatants[anim_target_idx]["entity"]
            start_pos = pos
            target_pos = entity_pos.get(id(target_entity))
            if target_pos:
                move_vector = (target_pos[0] - start_pos[0] + 140, target_pos[1] - start_pos[1])
                if anim_phase == 1:
                    progress = anim_phase_frame / ANIM_PHASE_FRAMES
                    offset_x = move_vector[0] * progress
                    offset_y = move_vector[1] * progress
                elif anim_phase == 2:
                    offset_x = move_vector[0]
                    offset_y = move_vector[1]
                elif anim_phase == 3:
                    progress = 1 - (anim_phase_frame / ANIM_PHASE_FRAMES)
                    offset_x = move_vector[0] * progress
                    offset_y = move_vector[1] * progress

        # 目标选择高亮（只高亮活着的敌人）
        if battle_sub_state == BATTLE_STATE_TARGET and enemy["hp"] > 0:
            pygame.draw.rect(surface, YELLOW, (*pos, formation.SLOT_WIDTH, formation.SLOT_HEIGHT), 3)

        # 选择头像（攻击图片阶段用进攻头像）
        if anim_active and anim_phase == 2:
            img = load_attack_avatar(enemy["name"], size=(80, 120))
        else:
            img = load_avatar(enemy["name"], size=(80, 120))

        draw_pos = (pos[0] + offset_x, pos[1] + offset_y)
        if img:
            surface.blit(img, draw_pos)
        else:
            pygame.draw.rect(surface, RED, (*draw_pos, 80, 120))

        # 绘制名称和HP
        name_color = YELLOW if is_current else RED
        draw_text(surface, enemy["name"], FONT_SMALL[1], name_color, pos[0] + formation.SLOT_WIDTH * 2, pos[1] + formation.SLOT_HEIGHT//2 - 20)
        hp_text = f"HP: {max(0, enemy['hp'])}/{enemy['max_hp']}"
        draw_text(surface, hp_text, FONT_SMALL[1], name_color, pos[0] + formation.SLOT_WIDTH * 2, pos[1] + formation.SLOT_HEIGHT//2 + 20)

        if enemy["hp"] <= 0:
            s = pygame.Surface((formation.SLOT_WIDTH, formation.SLOT_HEIGHT))
            s.set_alpha(128)
            s.fill(GRAY)
            surface.blit(s, pos)

    # 绘制战斗按钮（与之前相同）
    margin = 20
    button_y = SCREEN_HEIGHT - 60 - margin
    btn_width, btn_height = 150, 60
    btn_spacing = 10
    x_attack = margin
    x_skill = x_attack + btn_width + btn_spacing
    x_run = x_skill + btn_width + btn_spacing

    current_is_player = (combatants[current_index]["type"] == "player") if combatants else False
    btn_attack_color = BLUE if current_is_player else GRAY
    btn_skill_color = PURPLE if current_is_player else GRAY

    draw_button(surface, pygame.Rect(x_attack, button_y, btn_width, btn_height),
                "攻击", FONT_MEDIUM[1], GRAY, btn_attack_color, WHITE)
    draw_button(surface, pygame.Rect(x_skill, button_y, btn_width, btn_height),
                "技能(治疗)", FONT_MEDIUM[1], GRAY, btn_skill_color, WHITE)
    draw_button(surface, pygame.Rect(x_run, button_y, btn_width, btn_height),
                "逃跑", FONT_MEDIUM[1], GRAY, GRAY, WHITE)
    # =================================

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

