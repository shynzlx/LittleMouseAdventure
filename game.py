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

# 战斗相关变量
combatants = []                  # 战斗单位列表
current_index = 0                # 当前行动者索引
battle_sub_state = BATTLE_STATE_ACTION   # 战斗子状态
anim_attacker_idx = None         # 攻击者索引
anim_target_idx = None           # 目标索引
anim_phase = 0                   # 动画阶段
anim_phase_frame = 0             # 动画帧计数
anim_frame = 0                   # 旧版动画帧（可能废弃，但保留）

# 上阵界面相关
formation_selected_role_index = -1      # 当前选中的角色在 player_team 中的索引，-1表示未选中
formation_step = 0                      # 0: 等待选择角色, 1: 等待选择站位
formation_scroll = 0                    # 上阵界面角色列表滚动偏移

# 玩家队伍和背包（由存档加载）
player_team = []
inventory = {}

# ----- 初始化函数 -----
def init_game():
    """加载存档并初始化角色数据（原 main.py 中的初始化代码）"""
    global player_team, inventory, current_level
    player_team, inventory, current_level = save.load_game()

    # 以下是从 main.py 复制的角色数据补全代码
    role_pool = load_all_roles()
    role_base_map = {role["name"]: role for role in role_pool}

    for role in player_team:
        base = role_base_map.get(role["name"])
        if base:
            for key, value in base.items():
                if key not in role:
                    role[key] = value

    # 为所有角色添加 active 字段（如果没有）
    for i, role in enumerate(player_team):
        if "active" not in role:
            role["active"] = (i < MAX_ACTIVE)

    # 为所有角色添加 speed 字段（如果没有）
    for role in player_team:
        if "speed" not in role:
            role["speed"] = role.get("stamina", 50)
    
     # 为所有角色添加 slot 字段（如果没有），-1表示未上阵
    for role in player_team:
        if "slot" not in role:
            role["slot"] = -1

    # 根据旧的 active 字段初始化 slot（兼容旧存档）
    next_slot = 0
    for role in player_team:
        if role.get("active", False):
            if next_slot < MAX_ACTIVE:
                role["slot"] = next_slot
                next_slot += 1
            else:
                role["active"] = False  # 超过上限的设为False

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
    
def save_game():
    """保存游戏（调用 save 模块）"""
    save.save_game(player_team, inventory, current_level)
    print("游戏已保存")

def add_reward(reward):
    """将奖励添加到背包"""
    global inventory
    for key, value in reward.items():
        inventory[key] = inventory.get(key, 0) + value