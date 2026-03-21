# game.py - 全局游戏状态和核心函数
# 所有模块通过导入此文件来访问和修改游戏状态，避免循环导入

import save
from constants import *
from characters import load_all_roles

# ----- 全局变量 -----
# 这些变量原本在 main.py 中，现在集中管理
game_state = STATE_MENU          # 当前游戏状态
prev_state = game_state          # 前一状态（用于音乐切换）
current_music = None             # 当前播放的音乐
win_reward = None                # 胜利奖励
current_level = 1                # 当前关卡编号
enemies = []                     # 当前敌人列表
selected_role_index = 0          # 养成界面选中的角色索引
gacha_result = None              # 抽卡结果
upgrade_scroll = 0               # 养成界面滚动偏移
confirm_level = 1                # 待确认的关卡
current_skill_points = 0         # 战斗技能点
damage_numbers = []              # 伤害数字动画列表
#战斗消息 
battle_messages = []           # 每个元素为 (文本, 剩余帧数)
MAX_MESSAGES = 5               # 最多显示5条

# 技能目标选择
target_selection_mode = False      # 是否处于选择目标模式
pending_skill = None               # 待释放的技能信息（技能字典）
selectable_targets = []            # 可选目标的索引列表（根据技能类型决定是 player_team 索引还是敌人索引）

# 战斗相关变量
combatants = []                  # 战斗单位列表
current_index = 0                # 当前行动者索引
battle_sub_state = BATTLE_STATE_ACTION   # 战斗子状态
anim_attacker_idx = None         # 攻击者索引
anim_target_idx = None           # 目标索引
anim_phase = 0                   # 动画阶段
anim_phase_frame = 0             # 动画帧计数
anim_frame = 0                   # 旧版动画帧（可能废弃，但保留）
anim_skill = None                # 当前动画对应的技能字典
anim_skill_target_idx = None     # 技能目标在 player_team 或 enemies 中的索引
anim_is_skill = False            # 当前动画是否为技能（用于区分头像）
anim_mode = "move"                # 当前动画模式："move" 或 "shake"
current_exp_reward = 0

# 上阵界面相关
formation_selected_role_index = -1      # 当前选中的角色在 player_team 中的索引，-1表示未选中
formation_step = 0                      # 0: 等待选择角色, 1: 等待选择站位
formation_scroll = 0                    # 上阵界面角色列表滚动偏移

# 玩家队伍和背包（由存档加载）
player_team = []
inventory = {}

# ----- 初始化函数 -----
def init_game():
    global player_team, inventory, current_level
    player_team, inventory, current_level = save.load_game()

    # 加载我方角色基础数据
    friendly_roles = load_all_roles()  # 从 characters.py 导入
    role_base_map = {role["name"]: role for role in friendly_roles}

    for role in player_team:
        base = role_base_map.get(role["name"])
        if base:
            # 补全缺失字段（如技能、颜色等）
            for key, value in base.items():
                if key not in role and key not in ("base_stats", "growth"):
                    role[key] = value
            # 特别处理故事：用基础角色的故事覆盖存档中的故事
            if "story" in base:
                role["story"] = base["story"]
            # 同步技能数据
            base_skills = base.get("skills", [])
            for i, skill in enumerate(role.get("skills", [])):
                if i < len(base_skills):
                    base_skill = base_skills[i]
                    # 1. 补全缺失字段（原有逻辑）
                    for k, v in base_skill.items():
                        if k not in skill:
                            skill[k] = v
                    # 2. 根据基础配置中的 prof_to_next 重新计算当前等级的所需经验
                    if "prof_to_next" in base_skill:
                        base_prof = base_skill["prof_to_next"]
                        level = skill.get("level", 1)
                        # 公式：当前等级所需经验 = 基础经验 × (1.6 ^ (等级-1))
                        skill["prof_to_next"] = int(base_prof * (1.6 ** (level - 1)))
                    # 注意：不覆盖 proficiency（熟练度），保留存档中的值

    # 为所有角色添加 active 字段（如果没有）
    for i, role in enumerate(player_team):
        if "active" not in role:
            role["active"] = (i < MAX_ACTIVE)

    # 为所有角色添加 slot 字段（如果没有），-1表示未上阵
    # 并根据 slot 设置 active 字段
    for role in player_team:
        if "slot" not in role:
            role["slot"] = -1
        # 根据 slot 确定上阵状态
        role["active"] = (0 <= role["slot"] < MAX_ACTIVE)

    # 新增：确保每个角色都有 fatigue 字段
    for role in player_team:
        if "fatigue" not in role:
            role["fatigue"] = 0

# ----- 状态修改函数 -----
def set_state(new_state):
    """安全地修改游戏状态"""
    global game_state, prev_state
    prev_state = game_state
    game_state = new_state

def reset_formation():
    """重置上阵界面状态"""
    global formation_selected_role_index, formation_step, formation_scroll
    formation_selected_role_index = -1
    formation_step = 0
    formation_scroll = 0

def get_active_team():
    """返回一个长度为 MAX_ACTIVE 的列表，每个元素是站在对应槽位的角色或 None"""
    active_slots = [None] * MAX_ACTIVE
    for role in player_team:
        slot = role.get("slot", -1)
        if 0 <= slot < MAX_ACTIVE:
            active_slots[slot] = role
    return active_slots

def assign_role_to_slot(role_index, slot):
    """
    将 player_team[role_index] 放置到指定槽位 slot (0-5)
    如果该槽位已有角色，则原角色槽位设为 -1（下阵）
    """
    global player_team
    role = player_team[role_index]
    # 检查目标槽位是否已有角色
    for r in player_team:
        if r.get("slot") == slot:
            r["slot"] = -1
            r["active"] = False
            break
    # 设置新角色的槽位和 active
    role["slot"] = slot
    role["active"] = True

def remove_role_from_slot(slot):
    """将指定槽位的角色下阵"""
    for role in player_team:
        if role.get("slot") == slot:
            role["slot"] = -1
            role["active"] = False
            return True
    return False
    
def save_game():
    """保存游戏（调用 save 模块）"""
    save.save_game(player_team, inventory, current_level)
    print("游戏已保存")

def add_reward(reward):
    """将奖励添加到背包"""
    global inventory
    for key, value in reward.items():
        inventory[key] = inventory.get(key, 0) + value

def add_damage_number(pos, value, color=RED):
    damage_numbers.append({
        "pos": pos,
        "value": value,
        "color": color,
        "frame": 0,
        "max_frame": 20,
        "offset_y": 0
    })

def update_damage_numbers():
    """更新伤害数字动画，返回是否还有活跃的数字"""
    global damage_numbers
    from constants import FONT_MEDIUM
    import pygame
    font = pygame.font.Font(FONT_MEDIUM[0], FONT_MEDIUM[1])

    for d in damage_numbers[:]:
        color = d["color"]
        # 根据颜色判断符号：绿色为治疗（+），其他为伤害（-）
        sign = "-"
        if color == GREEN:
            sign = "+"
        text_surf = font.render(f"{sign}{d['value']}", True, color)
        d["frame"] += 1
        d["offset_y"] = -d["frame"] * 1  # 向上移动
        if d["frame"] >= d["max_frame"]:
            damage_numbers.remove(d)
    return len(damage_numbers) > 0

def add_battle_message(text):
    """添加一条战斗消息，自动移除最旧的消息"""
    battle_messages.append(text)
    if len(battle_messages) > MAX_MESSAGES:
        battle_messages.pop(0)

def update_battle_messages():
    """更新消息的剩余帧数，移除过期的"""
    global battle_messages
    for msg in battle_messages[:]:
        msg[1] -= 1
        if msg[1] <= 0:
            battle_messages.remove(msg)