# battle.py - 回合制战斗逻辑

import random
from constants import *

def calculate_remaining_time(speed):
    """根据速度计算初始剩余时间"""
    return BASE_TIME / speed if speed > 0 else BASE_TIME

def initialize_combatants(player_team, enemy):
    """初始化战斗单位列表，包含所有上阵角色和敌人"""
    combatants = []
    # 添加玩家角色
    # 玩家角色：按上阵顺序分配站位索引 0~5
    for idx, role in enumerate(player_team):
        speed = role.get("speed", role.get("stamina", 50))
        combatants.append({
            "type": "player",
            "entity": role,
            "speed": speed,
            "remaining_time": calculate_remaining_time(speed),
            "slot_index": idx   # 站位索引
        })
    # 敌人：目前只有一个，固定站位索引0
    enemy_speed = enemy.get("speed", 30)
    combatants.append({
        "type": "enemy",
        "entity": enemy,
        "speed": enemy_speed,
        "remaining_time": calculate_remaining_time(enemy_speed),
        "slot_index": 0
    })
    return combatants

def update_combatants(combatants, current_index):
    """
    当前行动者行动后，更新所有单位的剩余时间
    规则：
    1. 将当前行动者的剩余时间重置为 BASE_TIME / speed
    2. 其他所有单位的剩余时间减去当前行动者行动前的剩余时间
    3. 确保剩余时间不小于0
    """
    current = combatants[current_index]
    action_time = current["remaining_time"]  # 当前单位行动前的剩余时间

    # 重置当前单位的剩余时间
    current["remaining_time"] = calculate_remaining_time(current["speed"])

    # 其他单位减去 action_time
    for i, c in enumerate(combatants):
        if i != current_index:
            c["remaining_time"] = max(0, c["remaining_time"] - action_time)

def get_next_attacker(combatants):
    """返回剩余时间最小的单位的索引"""
    min_time = float('inf')
    next_index = 0
    for i, c in enumerate(combatants):
        if c["remaining_time"] < min_time:
            min_time = c["remaining_time"]
            next_index = i
    return next_index

def player_attack(combatants, current_index, enemy, skill_points):
    """玩家角色攻击敌人"""
    attacker = combatants[current_index]["entity"]
    # 计算伤害（沿用原有公式）
    dmg = random.randint(20, 40) + attacker["atk"]  # 简化：只考虑自身攻击
    enemy["hp"] -= dmg
    print(f"{attacker['name']} 攻击！造成 {dmg} 伤害，敌人剩余 HP: {enemy['hp']}")
    # 攻击后更新剩余时间
    update_combatants(combatants, current_index)
    skill_points += 1
    # 返回胜利状态
    if enemy["hp"] <= 0:
        return "win", skill_points
    return "continue", skill_points

def player_skill(combatants, current_index, player_team, skill_points):
    """玩家角色使用技能（治疗）"""
    if skill_points <= 0:
        print("技能点不足！")
        return "no_skill", skill_points   # 新增状态表示技能点不足    
    attacker = combatants[current_index]["entity"]
    heal = random.randint(20, 35)
    for role in player_team:
        if role["hp"] > 0:
            role["hp"] = min(role["max_hp"], role["hp"] + heal)
    print(f"{attacker['name']} 使用治疗！全体治疗 {heal} HP")
    # 治疗后更新剩余时间
    update_combatants(combatants, current_index)
    skill_points -= 1
    return "continue", skill_points

def enemy_attack(combatants, current_index, player_team):
    """敌人攻击玩家队伍"""
    enemy = combatants[current_index]["entity"]
    # 只选择活着的玩家角色
    alive_team = [r for r in player_team if r["hp"] > 0]
    if not alive_team:
        return "lose"
    target = random.choice(alive_team)
    dmg = random.randint(15, 30)
    target["hp"] = max(0, target["hp"] - dmg)
    print(f"{enemy['name']} 攻击 {target['name']}，造成 {dmg} 伤害")
    # 攻击后更新剩余时间
    update_combatants(combatants, current_index)
    # 检查队伍是否全灭
    if all(r["hp"] <= 0 for r in player_team):
        return "lose"
    return "continue"
def reset_team_hp(team):
    """将所有角色的HP回满"""
    for role in team:
        role["hp"] = role["max_hp"]