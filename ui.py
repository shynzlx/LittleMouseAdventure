# ui.py - 所有绘制函数

import pygame
from constants import *
import avatar_mapper      # 初始化映射
import formation
import game               # 新增：访问游戏状态
import button             # 新增：使用按钮类
# 头像缓存
avatar_cache = {}

# 当前界面的按钮列表（新增）
current_buttons = []

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

def load_skill_avatar(role_name, size=(180, 270)):
    filename = avatar_mapper.get_skill_avatar_filename(role_name)
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
            print(f"技能头像加载失败: {full_path} - {e}")
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
    # 此函数保留但不再被按钮绘制使用，保留以供其他非按钮元素使用
    pygame.draw.rect(surface, bg_color, rect, border_radius=15)
    pygame.draw.rect(surface, border_color, rect, 5, border_radius=15)
    draw_text(surface, text, font_size, text_color, rect.centerx, rect.centery)

def draw_hp_bar(surface, x, y, current, max_val, width=200, height=20, color=RED):
    bar_rect = pygame.Rect(x, y, width, height)
    fill_width = (current / max_val) * width if max_val > 0 else 0
    pygame.draw.rect(surface, GRAY, bar_rect)
    pygame.draw.rect(surface, color, (x, y, fill_width, height))


# 绘制主菜单
def draw_menu(surface):
    global current_buttons
    current_buttons.clear()   # 清空上一界面的按钮

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

    # 创建按钮对象并添加到 current_buttons
    # 闯关模式按钮
    btn1 = button.Button(
        rect=(btn_x, 250, BTN_WIDTH, BTN_HEIGHT),
        text="闯关模式", font_size=FONT_BIG[1],
        bg_color=GREEN, border_color=GREEN, text_color=WHITE,
        bg_alpha=80,
        callback=lambda: game.set_state(STATE_CHALLENGE)
    )
    current_buttons.append(btn1)

    # 保存游戏按钮
    btn2 = button.Button(
        rect=(btn_x, 400, BTN_WIDTH, BTN_HEIGHT),
        text="保存游戏", font_size=FONT_BIG[1],
        bg_color=BLUE, border_color=BLUE, text_color=WHITE,
        bg_alpha=180,
        callback=game.save_game
    )
    current_buttons.append(btn2)

    # 大世界按钮
    btn3 = button.Button(
        rect=(btn_x, 550, BTN_WIDTH, BTN_HEIGHT),
        text="大世界（敬请期待）", font_size=FONT_BIG[1],
        bg_color=(150,150,150), border_color=(150,150,150), text_color=WHITE,
        callback=lambda: game.set_state(STATE_WORLD)
    )
    current_buttons.append(btn3)

    # 右下角抽卡按钮
    margin = 20
    bottom_y = SCREEN_HEIGHT - MENU_BTN_HEIGHT - margin
    gacha_rect = pygame.Rect(SCREEN_WIDTH - MENU_BTN_WIDTH - margin, bottom_y, MENU_BTN_WIDTH, MENU_BTN_HEIGHT)
    btn4 = button.Button(
        rect=gacha_rect,
        text="抽卡", font_size=15,
        bg_color=ORANGE, border_color=YELLOW, text_color=WHITE,
        callback=lambda: game.set_state(STATE_GACHA)
    )
    current_buttons.append(btn4)

    # 角色养成按钮
    upgrade_rect = pygame.Rect(gacha_rect.left - MENU_BTN_WIDTH - margin + 25, bottom_y, MENU_BTN_WIDTH, MENU_BTN_HEIGHT)
    btn5 = button.Button(
        rect=upgrade_rect,
        text="角色养成", font_size=15,
        bg_color=PURPLE, border_color=WHITE, text_color=WHITE,
        callback=lambda: game.set_state(STATE_UPGRADE)
    )
    current_buttons.append(btn5)

    # 上阵按钮（放在抽卡和角色养成之间）
    formation_rect = pygame.Rect(upgrade_rect.left - MENU_BTN_WIDTH - margin + 25, bottom_y, MENU_BTN_WIDTH, MENU_BTN_HEIGHT)
    btn6 = button.Button(
        rect=formation_rect,
        text="上阵", font_size=15,
        bg_color=GREEN, border_color=WHITE, text_color=WHITE,
        callback=lambda: game.set_state(STATE_FORMATION)
    )
    current_buttons.append(btn6)

    # 绘制所有按钮
    for btn in current_buttons:
        btn.draw(surface)

    # 显示金币
    draw_text(surface, f"金币: {game.inventory.get('gold', 0)}", FONT_MEDIUM[1], BLACK, SCREEN_WIDTH - 220, 30)
    # 底部提示
    draw_text(surface, "点击按钮开始冒险！", FONT_MEDIUM[1], RED, SCREEN_WIDTH//2, 680)


# 绘制闯关模式
def draw_challenge(surface):
    global current_buttons
    current_buttons.clear()

    draw_text(surface, "闯关模式", FONT_TITLE[1], GREEN, SCREEN_WIDTH//2, 120)
    draw_text(surface, "选择关卡", FONT_BIG[1], WHITE, SCREEN_WIDTH//2, 250)

    btn_x = (SCREEN_WIDTH - BTN_WIDTH) // 2

    # 返回主菜单按钮
    back_btn = button.Button(
        rect=(50, SCREEN_HEIGHT-100, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT),
        text="返回主菜单", font_size=FONT_MEDIUM[1],
        bg_color=GRAY, border_color=RED, text_color=WHITE,
        callback=lambda: game.set_state(STATE_MENU)
    )
    current_buttons.append(back_btn)

    # 关卡1
    btn1 = button.Button(
        rect=(btn_x - 100, 350, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT),
        text="关卡1", font_size=FONT_MEDIUM[1],
        bg_color=GRAY, border_color=GREEN, text_color=WHITE,
        callback=lambda: confirm_level(1)   # 下面定义
    )
    current_buttons.append(btn1)

    # 关卡2
    btn2 = button.Button(
        rect=(btn_x + 150, 350, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT),
        text="关卡2", font_size=FONT_MEDIUM[1],
        bg_color=GRAY, border_color=GREEN, text_color=WHITE,
        callback=lambda: confirm_level(2)
    )
    current_buttons.append(btn2)

    # 关卡3
    btn3 = button.Button(
        rect=(btn_x + 400, 350, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT),
        text="关卡3", font_size=FONT_MEDIUM[1],
        bg_color=GRAY, border_color=GREEN, text_color=WHITE,
        callback=lambda: confirm_level(3)
    )
    current_buttons.append(btn3)

    # 绘制所有按钮
    for btn in current_buttons:
        btn.draw(surface)

def confirm_level(level):
    """进入确认界面（辅助函数）"""
    game.confirm_level = level
    game.set_state(STATE_CONFIRM)


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

def on_skill_click():
    if game.combatants and game.combatants[game.current_index]["type"] == "player":
        if game.current_skill_points <= 0:
            print("技能点不足！")
            game.add_battle_message("技能点不足！")
            return
        current_entity = game.combatants[game.current_index]["entity"]
        skills = current_entity.get("skills")
        if not skills:
            print("没有技能")
            return
        skill_info = skills[0]  # 取第一个技能

        # 根据技能目标类型处理
        if skill_info["target"] == "single":
            # 需要选择目标
            game.target_selection_mode = True
            game.pending_skill = skill_info
            # 设置可选目标列表（实体对象本身）
            if skill_info["type"] == "heal":
                game.selectable_targets = [role for role in game.player_team if role["hp"] > 0]
            elif skill_info["type"] == "attack":
                game.selectable_targets = [enemy for enemy in game.enemies if enemy["hp"] > 0]
        else:
            # 不需要目标的技能（如嘲讽、增益等），直接触发动画
            game.anim_is_skill = True
            game.anim_mode = "shake"                 # 使用晃动动画
            game.anim_skill = skill_info              # 存储技能信息，动画结束后执行
            game.anim_skill_target_idx = None         # 表示技能不需要目标
            game.anim_attacker_idx = game.current_index
            game.anim_target_idx = game.current_index # 目标设置为自身（用于动画，但实际不移动）
            game.anim_phase = 1
            game.anim_phase_frame = 0
            game.battle_sub_state = BATTLE_STATE_ANIM

def on_cancel_skill():
    game.target_selection_mode = False
    game.pending_skill = None
    # 无需其他操作，下次绘制时按钮会变回技能

# ui.py - 重写 draw_battle 函数
import formation
def draw_battle(surface):
    global current_buttons
    current_buttons.clear()

    # 从 game 模块获取数据
    player_team = game.get_active_team()
    enemies = game.enemies
    current_level = game.current_level
    combatants = game.combatants
    current_index = game.current_index
    skill_points = game.current_skill_points
    battle_sub_state = game.battle_sub_state
    anim_attacker_idx = game.anim_attacker_idx
    anim_target_idx = game.anim_target_idx
    anim_phase = game.anim_phase
    anim_phase_frame = game.anim_phase_frame

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
        if anim_active:
            if game.anim_mode == "move":
                if anim_target_idx is not None:
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
            elif game.anim_mode == "shake":
            # 原地晃动动画：在阶段2和阶段3持续晃动，使用正弦波
                if anim_phase == 2 or anim_phase == 3:
                    import math  # 确保文件顶部已导入，或在此处临时导入
                    # 计算当前在整个晃动阶段（阶段2+3）的进度 (0~1)
                    total_shake_frames = ANIM_PHASE_FRAMES * 2  # 阶段2和3的总帧数
                    current_shake_frame = anim_phase_frame
                    if anim_phase == 3:
                        current_shake_frame += ANIM_PHASE_FRAMES
                    progress = current_shake_frame / total_shake_frames
                    amplitude = 10  # 晃动幅度（像素），可自行调整
                    # 正弦波，一个完整周期对应整个晃动阶段
                    shift = amplitude * math.sin(progress * 2 * math.pi)
                    offset_x = int(shift)
                    # offset_y 保持0（如果需要上下晃动可添加）

        # 选择头像（攻击阶段使用进攻图片）
                # 选择头像（根据动画状态和技能标志）
               # 选择头像（根据动画状态和技能标志）
        if anim_active:
            if game.anim_is_skill:
                if game.anim_mode == "move":
                    # 攻击技能：阶段2用技能头像，其他用普通头像
                    if anim_phase == 2:
                        img = load_skill_avatar(role["name"], size=(80, 120))
                    else:
                        img = load_avatar(role["name"], size=(80, 120))
                else:  # "shake" 或其他模式（治疗、嘲讽等）
                    # 非攻击技能全程用技能头像
                    img = load_skill_avatar(role["name"], size=(80, 120))
            else:
                # 普通攻击：阶段2用攻击头像，其他用普通头像
                if anim_phase == 2:
                    img = load_attack_avatar(role["name"], size=(80, 120))
                else:
                    img = load_avatar(role["name"], size=(80, 120))
        else:
            img = load_avatar(role["name"], size=(80, 120))
            
        draw_pos = (pos[0] + offset_x, pos[1] + offset_y)
        if img:
            surface.blit(img, draw_pos)
        else:
            pygame.draw.rect(surface, role["color"], (*draw_pos, 80, 120))

        # 目标选择高亮（新增，基于 game.target_selection_mode 和实体比较）
        if game.target_selection_mode and role in game.selectable_targets:
            pygame.draw.rect(surface, YELLOW, (*pos, formation.SLOT_WIDTH, formation.SLOT_HEIGHT), 5)

        name_color = GRAY if role["hp"] <= 0 else (YELLOW if is_current else WHITE)

        # 绘制名称和HP（保持在原位置，不随角色移动）
        # 名称和等级合并
        name_level_text = f"{role['name']} Lv.{role['level']}"
        draw_text(surface, name_level_text, 20, name_color, pos[0] + formation.SLOT_WIDTH * 2, pos[1] + formation.SLOT_HEIGHT//2 - 20)
        # 血量（字号也调小）
        hp_display = max(0, role["hp"])
        hp_text = f"HP: {hp_display}/{role['max_hp']}"
        draw_text(surface, hp_text, 20, name_color, pos[0] + formation.SLOT_WIDTH * 2, pos[1] + formation.SLOT_HEIGHT//2 + 20)

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

        # 目标选择高亮（替换原有基于 battle_sub_state 的判断，使用新变量）
        if game.target_selection_mode and enemy in game.selectable_targets:
            pygame.draw.rect(surface, YELLOW, (*pos, formation.SLOT_WIDTH, formation.SLOT_HEIGHT), 5)

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
        # 显示敌人名称和等级（字号20）
        name_level_text = f"{enemy['name']} Lv.{enemy.get('level', 1)}"
        draw_text(surface, name_level_text, 20, name_color, pos[0] + formation.SLOT_WIDTH * 2, pos[1] + formation.SLOT_HEIGHT//2 - 20)
        # 显示血量（字号20）
        hp_text = f"HP: {max(0, enemy['hp'])}/{enemy['max_hp']}"
        draw_text(surface, hp_text, 20, name_color, pos[0] + formation.SLOT_WIDTH * 2, pos[1] + formation.SLOT_HEIGHT//2 + 20)
        if enemy["hp"] <= 0:
            s = pygame.Surface((formation.SLOT_WIDTH, formation.SLOT_HEIGHT))
            s.set_alpha(128)
            s.fill(GRAY)
            surface.blit(s, pos)

    # 绘制伤害数字
    for d in game.damage_numbers:
        x, y = d["pos"]
        y += d["offset_y"]
        # 根据帧数计算透明度
        alpha = 255 - 0.5 * int(255 * d["frame"] / d["max_frame"])
        # 创建字体并渲染数字
        font = pygame.font.Font(FONT_MEDIUM[0], FONT_MEDIUM[1])
        text_surf = font.render(f"-{d['value']}", True, d.get("color", RED))
        text_surf.set_alpha(alpha)
        text_rect = text_surf.get_rect(center=(x, y + 50))
        surface.blit(text_surf, text_rect)

    # 绘制战斗按钮（作为按钮对象）
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

    # 判断按钮是否可用（动画期间不可用）
    buttons_enabled = (battle_sub_state != BATTLE_STATE_ANIM)

    # 攻击按钮
    attack_border = btn_attack_color if buttons_enabled else GRAY
    attack_callback = on_attack_click if buttons_enabled else None
    attack_btn = button.Button(
        rect=(x_attack, button_y, btn_width, btn_height),
        text="攻击", font_size=FONT_MEDIUM[1],
        bg_color=GRAY, border_color=attack_border, text_color=WHITE,
        callback=attack_callback
    )
    current_buttons.append(attack_btn)

    # 技能按钮（需要先获取技能名称）
    skill_name = "技能"
    if combatants and current_index < len(combatants):
        current = combatants[current_index]
        if current["type"] == "player":
            entity = current["entity"]
            skills = entity.get("skills")
            if skills and len(skills) > 0:
                skill_name = skills[0]["name"]

    if game.target_selection_mode:
        skill_text = "取消"
        skill_callback = on_cancel_skill
        skill_border = RED
    else:
        skill_text = skill_name
        skill_callback = on_skill_click if buttons_enabled else None
        skill_border = btn_skill_color if buttons_enabled else GRAY

    skill_btn = button.Button(
        rect=(x_skill, button_y, btn_width, btn_height),
        text=skill_text, font_size=FONT_MEDIUM[1],
        bg_color=GRAY, border_color=skill_border, text_color=WHITE,
        callback=skill_callback
    )
    current_buttons.append(skill_btn)

    # 逃跑按钮
    run_callback = on_run_click if buttons_enabled else None
    run_btn = button.Button(
        rect=(x_run, button_y, btn_width, btn_height),
        text="逃跑", font_size=FONT_MEDIUM[1],
        bg_color=GRAY, border_color=GRAY, text_color=WHITE,
        callback=run_callback
    )
    # 确保按钮被添加到列表
    current_buttons.append(skill_btn)
    #print(f"技能按钮已添加，文本: {skill_btn.text}")  # 调试输出

    # 逃跑按钮
    run_btn = button.Button(
        rect=(x_run, button_y, btn_width, btn_height),
        text="逃跑", font_size=FONT_MEDIUM[1],
        bg_color=GRAY, border_color=GRAY, text_color=WHITE,
        callback=on_run_click
    )
    current_buttons.append(run_btn)

    # 绘制所有按钮
    for btn in current_buttons:
        btn.draw(surface)
    
        # 绘制战斗消息（右下角）
    if game.battle_messages:
        msg_x = SCREEN_WIDTH - 425
        msg_y = SCREEN_HEIGHT - 175
        bg_height = len(game.battle_messages) * 30
        bg_surf = pygame.Surface((280, bg_height))
        bg_surf.set_alpha(128)
        bg_surf.fill(BLACK)
        surface.blit(bg_surf, (msg_x, msg_y - 5))
        for i, text in enumerate(game.battle_messages):
            # 最新一条用黄色，其余用白色
            color = YELLOW if i == len(game.battle_messages) - 1 else WHITE
            draw_text(surface, text, 18, color, msg_x + 10, msg_y + i * 30, center=False)

# 战斗按钮的回调函数（定义在ui.py中，以便访问game模块）
def on_attack_click():
    if game.combatants and game.combatants[game.current_index]["type"] == "player":
        # 进入目标选择模式，pending_skill 设为 None 表示普通攻击
        game.target_selection_mode = True
        game.pending_skill = None
        # 普通攻击的目标是所有存活的敌人实体
        game.selectable_targets = [c["entity"] for c in game.combatants if c["type"] == "enemy" and c["entity"]["hp"] > 0]

def on_run_click():
    from battle import reset_team_hp
    game.battle_messages.clear()
    reset_team_hp(game.player_team)
    game.set_state(STATE_CHALLENGE)


# 绘制养成界面（从 upgrade.py 调用）
# 绘制养成界面（从 upgrade.py 调用）
def draw_upgrade(surface):
    global current_buttons
    current_buttons.clear()

    # 从 game 获取数据
    player_team = game.player_team
    selected_role_index = game.selected_role_index
    inventory = game.inventory
    scroll = game.upgrade_scroll

    draw_text(surface, "角色养成", FONT_TITLE[1], YELLOW, SCREEN_WIDTH//2, 60)

    # 计算可见角色范围
    visible_count = 7  # 一次最多显示7个（与上阵界面一致）
    start_idx = scroll
    end_idx = min(start_idx + visible_count, len(player_team))
    visible_roles = player_team[start_idx:end_idx]

    # 绘制角色列表（左侧）- 使用与上阵界面相同的样式
    left_list_x = 50
    left_list_y = 100
    slot_width = 200
    slot_height = 60
    spacing = 10

    y = left_list_y
    for i, role in enumerate(visible_roles):
        actual_idx = start_idx + i
        rect = pygame.Rect(left_list_x, y, slot_width, slot_height)

        # 背景色：选中时为红色，否则灰色
        bg_color = RED if actual_idx == selected_role_index else GRAY
        # 边框色：如果角色已上阵，用黄色；否则白色
        border_color = YELLOW if role.get("active", False) else WHITE

        role_btn = button.Button(
            rect=rect,
            text=role["name"], font_size=FONT_MEDIUM[1],
            bg_color=bg_color, border_color=border_color, text_color=WHITE,
            callback=lambda idx=actual_idx: select_role(idx)
        )
        current_buttons.append(role_btn)
        y += slot_height + spacing

    # 绘制滚动提示（如果有多页）
    if len(player_team) > visible_count:
        draw_text(surface, f"↑ 滚动查看 ({start_idx+1}-{end_idx}/{len(player_team)})", FONT_SMALL[1], RED, left_list_x + slot_width//2, left_list_y - 20)

    # 详细信息（右侧）- 以下代码保持不变
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
            # 获取效果值，如果不存在则显示 ?
            effect_value = sk.get('value', '?')
            text = f"{sk['name']} Lv.{sk['level']} ({sk['proficiency']}/{sk['prof_to_next']})"
            draw_text(surface, text, FONT_SMALL[1], WHITE, 400, sy)
            sy += 35

    # 道具按钮
    exp_btn = button.Button(
        rect=(600, 450, 180, 60),
        text=f"经验书 ({inventory['exp_book']})", font_size=FONT_MEDIUM[1],
        bg_color=GRAY, border_color=GREEN, text_color=WHITE,
        callback=lambda: use_exp_book(selected_role_index)
    )
    current_buttons.append(exp_btn)

    skill_btn = button.Button(
        rect=(800, 450, 180, 60),
        text=f"技能书 ({inventory['skill_book']})", font_size=FONT_MEDIUM[1],
        bg_color=GRAY, border_color=PURPLE, text_color=WHITE,
        callback=lambda: use_skill_book(selected_role_index)
    )
    current_buttons.append(skill_btn)

    # 返回主菜单按钮
    back_btn = button.Button(
        rect=(50, SCREEN_HEIGHT-100, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT),
        text="返回主菜单", font_size=FONT_MEDIUM[1],
        bg_color=GRAY, border_color=RED, text_color=WHITE,
        callback=lambda: game.set_state(STATE_MENU)
    )
    current_buttons.append(back_btn)

    # 绘制所有按钮
    for btn in current_buttons:
        btn.draw(surface)

# 养成界面辅助函数
def select_role(index):
    game.selected_role_index = index

def use_exp_book(index):
    from upgrade import use_exp_book as use
    use(index, game.player_team, game.inventory)

def use_skill_book(index):
    from upgrade import use_skill_book as use
    use(index, game.player_team, game.inventory)


# 绘制抽卡界面
def draw_gacha(surface):
    global current_buttons
    current_buttons.clear()

    draw_text(surface, "抽卡系统", FONT_TITLE[1], ORANGE, SCREEN_WIDTH//2, 120)

    # 抽卡按钮
    gacha_btn = button.Button(
        rect=((SCREEN_WIDTH-BTN_WIDTH)//2, 350, BTN_WIDTH, BTN_HEIGHT),
        text="抽卡一次", font_size=FONT_BIG[1],
        bg_color=GRAY, border_color=YELLOW, text_color=WHITE,
        callback=perform_gacha_callback
    )
    current_buttons.append(gacha_btn)

    # 显示抽卡结果（如果有）
    if game.gacha_result:
        draw_text(surface, f"抽到 {game.gacha_result['rarity']} 角色: {game.gacha_result['name']}",
                  FONT_BIG[1], game.gacha_result["color"], SCREEN_WIDTH//2, 500)

    # 返回按钮（左下角）
    back_btn = button.Button(
        rect=(50, SCREEN_HEIGHT-100, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT),
        text="返回主菜单", font_size=FONT_MEDIUM[1],
        bg_color=GRAY, border_color=RED, text_color=WHITE,
        callback=lambda: game.set_state(STATE_MENU)
    )
    current_buttons.append(back_btn)

    # 绘制所有按钮
    for btn in current_buttons:
        btn.draw(surface)

    # 在抽卡界面右上角显示金币
    draw_text(surface, f"金币: {game.inventory.get('gold', 0)}", FONT_MEDIUM[1], YELLOW, SCREEN_WIDTH - 150, 50)

def perform_gacha_callback():
    from gacha import perform_gacha
    result = perform_gacha(game.player_team, game.inventory)
    if result:
        game.gacha_result = result


# 绘制关卡确认对话框
def draw_confirm(surface):
    global current_buttons
    current_buttons.clear()

    level = game.confirm_level

    # 半透明遮罩
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    surface.blit(overlay, (0, 0))

    # 对话框背景
    dialog_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 100, 400, 200)
    pygame.draw.rect(surface, DARK_GRAY, dialog_rect, border_radius=10)
    pygame.draw.rect(surface, WHITE, dialog_rect, 3, border_radius=10)

    draw_text(surface, f"确定要进入关卡 {level} 吗？", FONT_MEDIUM[1], WHITE, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40)

    # 返回按钮
    return_btn = button.Button(
        rect=(SCREEN_WIDTH//2 - 140, SCREEN_HEIGHT//2 + 20, 120, 50),
        text="返回", font_size=FONT_MEDIUM[1],
        bg_color=GRAY, border_color=RED, text_color=WHITE,
        callback=lambda: game.set_state(STATE_CHALLENGE)
    )
    current_buttons.append(return_btn)

    # 出发按钮
    go_btn = button.Button(
        rect=(SCREEN_WIDTH//2 + 20, SCREEN_HEIGHT//2 + 20, 120, 50),
        text="出发！", font_size=FONT_MEDIUM[1],
        bg_color=GRAY, border_color=GREEN, text_color=WHITE,
        callback=start_battle
    )
    current_buttons.append(go_btn)

    for btn in current_buttons:
        btn.draw(surface)

def start_battle():
    """开始战斗，初始化 combatants 等"""
    game.battle_messages.clear() 
    active_team = game.get_active_team()
    if not active_team:
        print("没有上阵角色，无法战斗！")
        game.set_state(STATE_CHALLENGE)
        return
    from levels import setup_enemy
    from battle import initialize_combatants, get_next_attacker
    enemies, skill_points = setup_enemy(game.confirm_level)
    game.enemies = enemies
    game.combatants = initialize_combatants(active_team, enemies)
    game.current_index = get_next_attacker(game.combatants)
    game.current_skill_points = skill_points
    game.battle_sub_state = BATTLE_STATE_ACTION
    game.set_state(STATE_CHALLENGE_BATTLE)


# 绘制失败提示画面
def draw_lose(surface):
    global current_buttons
    current_buttons.clear()

    # 半透明遮罩
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    surface.blit(overlay, (0, 0))

    # 对话框背景
    dialog_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 100, 400, 200)
    pygame.draw.rect(surface, DARK_GRAY, dialog_rect, border_radius=10)
    pygame.draw.rect(surface, WHITE, dialog_rect, 3, border_radius=10)

    draw_text(surface, "你失败了！", FONT_BIG[1], RED, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40)

    # 确认按钮
    confirm_btn = button.Button(
        rect=(SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 + 20, 120, 50),
        text="确认", font_size=FONT_MEDIUM[1],
        bg_color=GRAY, border_color=GREEN, text_color=WHITE,
        callback=on_lose_confirm
    )
    current_buttons.append(confirm_btn)

    for btn in current_buttons:
        btn.draw(surface)

def on_lose_confirm():
    from battle import reset_team_hp
    reset_team_hp(game.player_team)
    game.combatants = []
    game.set_state(STATE_CHALLENGE)


# 绘制胜利界面
def draw_win(surface):
    global current_buttons
    current_buttons.clear()

    reward = game.win_reward

    # 收集奖励文本行
    reward_lines = []
    if reward:
        reward_lines.append(f"获得金币: {reward.get('gold', 0)}")
        reward_lines.append(f"获得经验书: {reward.get('exp_book', 0)}")
        reward_lines.append(f"获得技能书: {reward.get('skill_book', 0)}")
    line_count = len(reward_lines)

    # 基本尺寸设置
    title_height = 60          # 标题占用的高度
    line_height = 40           # 每行奖励文本的高度
    button_height = 50         # 按钮高度
    spacing = 20               # 间距

    # 计算对话框总高度
    dialog_height = title_height + button_height + spacing * 3 + line_count * line_height
    if dialog_height < 300:    # 最小高度
        dialog_height = 300

    # 对话框位置（水平居中，垂直居中）
    dialog_width = 400
    dialog_x = SCREEN_WIDTH // 2 - dialog_width // 2
    dialog_y = SCREEN_HEIGHT // 2 - dialog_height // 2
    dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)

    # 半透明遮罩
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    surface.blit(overlay, (0, 0))

    # 绘制对话框背景
    pygame.draw.rect(surface, DARK_GRAY, dialog_rect, border_radius=10)
    pygame.draw.rect(surface, WHITE, dialog_rect, 3, border_radius=10)

    # 绘制标题（对话框顶部）
    title_y = dialog_y + spacing + title_height // 2
    draw_text(surface, "战斗胜利！", FONT_BIG[1], YELLOW, SCREEN_WIDTH // 2, title_y)

    # 绘制奖励文本（标题下方）
    current_y = title_y + title_height // 2 + spacing
    for line in reward_lines:
        draw_text(surface, line, FONT_MEDIUM[1], YELLOW, SCREEN_WIDTH // 2, current_y)
        current_y += line_height

    # 绘制确认按钮（对话框底部）
    btn_y = dialog_y + dialog_height - button_height - spacing
    confirm_btn = button.Button(
        rect=(SCREEN_WIDTH // 2 - 60, btn_y, 120, 50),
        text="确认", font_size=FONT_MEDIUM[1],
        bg_color=GRAY, border_color=GREEN, text_color=WHITE,
        callback=lambda: game.set_state(STATE_CHALLENGE)
    )
    current_buttons.append(confirm_btn)

    for btn in current_buttons:
        btn.draw(surface)


# 绘制大世界界面（简单示例）
def draw_world(surface):
    draw_text(surface, "大世界模式", FONT_TITLE[1], BLUE, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50)
    draw_text(surface, "（开发中，按 ESC 返回）", FONT_MEDIUM[1], WHITE, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)

# ==================== 上阵界面 ===================
def draw_formation(surface):
    """
    绘制上阵界面（队伍配置）
    功能：
    - 左侧显示角色列表（可滚动点击）
    - 中间显示站位预览框（三行两列）
    - 底部提示文字
    - 返回主菜单按钮
    """
    global current_buttons
    current_buttons.clear()
    # 从 game 模块获取数据
    player_team = game.player_team
    scroll = game.formation_scroll          # 需要先在 game.py 中定义
    selected_idx = game.formation_selected_role_index  # 需要先在 game.py 中定义
    step = game.formation_step              # 需要先在 game.py 中定义
    # 绘制背景（纯黑）
    surface.fill(BLACK)
    # 绘制标题
    draw_text(surface, "队伍配置", FONT_TITLE[1], YELLOW, SCREEN_WIDTH//2, 50)
    # 绘制提示文字
    if step == 0:
        hint = "请选择角色"
    else:
        hint = "请选择它的站位"
    draw_text(surface, hint, FONT_BIG[1], CYAN, SCREEN_WIDTH//2, 120)
    # ========== 左侧角色列表（可滚动） ==========
    visible_count = 7  # 一次最多显示7个角色
    start_idx = scroll
    end_idx = min(start_idx + visible_count, len(player_team))
    visible_roles = player_team[start_idx:end_idx]

    left_list_x = 50
    left_list_y = 100
    slot_width = 200
    slot_height = 60
    spacing = 10
    for i, role in enumerate(visible_roles):
        actual_idx = start_idx + i
        y = left_list_y + i * (slot_height + spacing)
        rect = pygame.Rect(left_list_x, y, slot_width, slot_height)
        # 背景色：如果当前角色被选中，用角色颜色；否则灰色bg_color = RED if actual_idx == selected_idx else GRAY
        bg_color = RED if actual_idx == selected_idx else GRAY
        # 边框色：如果角色已上阵，用黄色；否则白色
        border_color = YELLOW if role.get("active", False) else WHITE
        # 创建按钮，点击时调用 select_formation_role(actual_idx)
        role_btn = button.Button(
            rect=rect,
            text=role["name"], font_size=FONT_MEDIUM[1],
            bg_color=bg_color, border_color=border_color, text_color=WHITE,
            callback=lambda idx=actual_idx: select_formation_role(idx)
        )
        current_buttons.append(role_btn)
    # 绘制滚动提示
    if len(player_team) > visible_count:
        draw_text(surface, f"↑ 滚动 ({start_idx+1}-{end_idx}/{len(player_team)})", FONT_SMALL[1], WHITE, left_list_x + slot_width//2, left_list_y - 20)

    # ========== 中间站位预览框 ==========
    # 复用战斗站位坐标，但整体向右偏移避免与左侧重叠
    offset_x = 300
    # 确保已导入 formation 模块（如果在文件顶部没有导入，需要添加 import formation）
    preview_slots = formation.PLAYER_POSITIONS

    for i, (x, y) in enumerate(preview_slots):
        rect = pygame.Rect(x + offset_x, y, formation.SLOT_WIDTH, formation.SLOT_HEIGHT)
        # 绘制框
        pygame.draw.rect(surface, GRAY, rect, 2)

        # 获取当前上阵角色（这里使用简单的按顺序填充，后续可改为真正的站位系统）
        active_team = game.get_active_team()
        if i < len(active_team) and active_team[i] is not None:
            role = active_team[i]
            img = load_avatar(role["name"], size=(formation.SLOT_WIDTH, formation.SLOT_HEIGHT))
            if img:
                surface.blit(img, (x + offset_x, y))
            else:
                pygame.draw.rect(surface, role["color"], rect)
            # 绘制角色名（可选）
            draw_text(surface, role["name"], FONT_SMALL[1], WHITE, rect.centerx, rect.centery - 20)
        else:
            # 空位显示编号
            draw_text(surface, str(i+1), FONT_SMALL[1], GRAY, rect.centerx, rect.centery)

    # ========== 返回主菜单按钮 ==========
    back_btn = button.Button(
        rect=(50, SCREEN_HEIGHT-100, BTN_SMALL_WIDTH, BTN_SMALL_HEIGHT),
        text="返回主菜单", font_size=FONT_MEDIUM[1],
        bg_color=GRAY, border_color=RED, text_color=WHITE,
        callback=lambda: game.set_state(STATE_MENU)
    )
    current_buttons.append(back_btn)

    # 绘制所有按钮
    for btn in current_buttons:
        btn.draw(surface)

# 上阵界面的辅助回调函数
def select_formation_role(index):
    """选择角色后进入选择站位阶段"""
    game.formation_selected_role_index = index
    game.formation_step = 1

def place_role_to_slot(slot_index):
    """
    将选中的角色放置到指定站位
    slot_index: 0-5 对应六个站位
    """
    if game.formation_selected_role_index == -1:
        return
    game.assign_role_to_slot(game.formation_selected_role_index, slot_index)
    game.formation_selected_role_index = -1
    game.formation_step = 0
#===========================================上阵界面结束===============================#