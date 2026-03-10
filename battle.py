# battle.py - 回合制战斗逻辑

import random
from constants import *

def calculate_remaining_time(speed):
    """根据速度计算初始剩余时间"""
    return BASE_TIME / speed if speed > 0 else BASE_TIME

def initialize_combatants(player_team, enemies):
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
    # 敌人
    for idx, enemy in enumerate(enemies):
        enemy_speed = enemy.get("speed", 30)
        combatants.append({
            "type": "enemy",
            "entity": enemy,
            "speed": enemy_speed,
            "remaining_time": calculate_remaining_time(enemy_speed),
            "slot_index": idx
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

def cleanup_combatants(combatants):
    """移除所有死亡单位，返回战斗结果"""
    original_len = len(combatants)
    combatants[:] = [c for c in combatants if c["entity"]["hp"] > 0]
    # 检查胜利/失败
    enemies_alive = any(c["type"] == "enemy" for c in combatants)
    players_alive = any(c["type"] == "player" for c in combatants)
    if not enemies_alive:
        return "win"
    if not players_alive:
        return "lose"
    return "continue"

def perform_attack(combatants, current_index, target_index, skill_points):
    """
    执行攻击（在动画结束后调用）
    返回 (result, next_index, new_skill_points)
    """
    attacker = combatants[current_index]["entity"]
    target_entity = combatants[target_index]["entity"]
    dmg = random.randint(20, 40) + attacker["atk"]
    target_entity["hp"] -= dmg
    print(f"{attacker['name']} 攻击 {target_entity['name']}，造成 {dmg} 伤害")

    result = cleanup_combatants(combatants)
    if result != "continue":
        return result, 0, skill_points

    # 重新定位攻击者索引（可能因死亡前移）
    new_current = None
    for i, c in enumerate(combatants):
        if c["entity"] is attacker:
            new_current = i
            break
    if new_current is None:
        return "lose", 0, skill_points

    update_combatants(combatants, new_current)
    skill_points += 1
    next_index = get_next_attacker(combatants)
    return "continue", next_index, skill_points

def player_skill(combatants, current_index, player_team, skill_points):
    if skill_points <= 0:
        print("技能点不足！")
        return "no_skill", current_index, skill_points   # 返回原索引，技能点不变

    attacker = combatants[current_index]["entity"]
    heal = random.randint(20, 35)
    for role in player_team:
        if role["hp"] > 0:
            role["hp"] = min(role["max_hp"], role["hp"] + heal)
    print(f"{attacker['name']} 使用治疗！全体治疗 {heal} HP")

    update_combatants(combatants, current_index)
    skill_points -= 1
    next_index = get_next_attacker(combatants)
    return "continue", next_index, skill_points

def enemy_attack(combatants, current_index, player_team):
    enemy = combatants[current_index]["entity"]
    alive_team = [r for r in player_team if r["hp"] > 0]
    if not alive_team:
        return "lose"
    target = random.choice(alive_team)
    dmg = random.randint(15, 30)
    target["hp"] = max(0, target["hp"] - dmg)
    print(f"{enemy['name']} 攻击 {target['name']}，造成 {dmg} 伤害")
    result = cleanup_combatants(combatants)
    if result != "continue":
        return result
    # 重新定位敌人索引
    new_current = None
    for i, c in enumerate(combatants):
        if c["entity"] is enemy:
            new_current = i
            break
    if new_current is None:
        return "lose"
    update_combatants(combatants, new_current)
    return "continue"

def reset_team_hp(team):
    """将所有角色的HP回满"""
    for role in team:
        role["hp"] = role["max_hp"]