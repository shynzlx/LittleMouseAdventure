# battle.py - 回合制战斗逻辑

import random
from constants import *
import game
import formation
from upgrade import add_exp_to_role, check_skill_upgrade


def calculate_remaining_time(speed):
    """根据速度计算初始剩余时间"""
    return BASE_TIME / speed if speed > 0 else BASE_TIME

def get_attack_factor():
    """
    返回伤害随机因子，范围 0.9 ~ 1.1，采用三角分布，众数 1.0。
    """
    return random.triangular(0.9, 1.1, 1.0)

def get_attack_multiplier(attacker):
    """
    根据攻击者的耐力和当前疲劳值计算伤害倍率。
    公式：
        若 fatigue <= 2，倍率 = 1；
        否则，倍率 = 1 / (1 + a * (fatigue - 2))
        其中 a = FATIGUE_DECAY_RATE / (1 + stamina / FATIGUE_STAMINA_FACTOR)
    """
    fatigue = attacker.get("fatigue", 0)
    stamina = attacker.get("stamina")  

    if fatigue <= 2:
        return 1.0

    stamina_factor = 1 + stamina / FATIGUE_STAMINA_FACTOR
    a = FATIGUE_DECAY_RATE / stamina_factor
    x = fatigue - 2
    multiplier = 1 / (1 + a * x)

    return multiplier  # 不设下限

def initialize_combatants(player_team, enemies):
    """初始化战斗单位列表，包含所有上阵角色和敌人"""
    combatants = []
    # 添加玩家角色
    # 玩家角色：按上阵顺序分配站位索引 0~5
    for slot_idx, role in enumerate(player_team):
        if role is None:
            continue
        speed = role.get("speed", role.get("stamina", 50))
        combatants.append({
            "type": "player",
            "entity": role,
            "speed": speed,
            "remaining_time": calculate_remaining_time(speed),
            "slot_index": slot_idx   # 站位索引
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

def grant_kill_rewards(attacker_entity, skill_used, killed_entities):
    """发放击杀奖励：角色经验+5/每个，技能击杀+3/每个"""
    if not killed_entities:
        return
    # 角色经验
    for _ in killed_entities:
        add_exp_to_role(attacker_entity, 5)
    # 技能击杀额外奖励
    if skill_used is not None:
        for _ in killed_entities:
            skill_used["proficiency"] = skill_used.get("proficiency", 0) + 3
            check_skill_upgrade(skill_used, attacker_entity)

def perform_attack(combatants, current_index, target_index, skill_points):
    attacker = combatants[current_index]["entity"]
    target_entity = combatants[target_index]["entity"]

    # 计算伤害（只计算一次）
    factor = get_attack_factor()
    base_dmg = int(attacker["atk"] * factor)
    mult = get_attack_multiplier(attacker)
    dmg = int(base_dmg * mult)
    dmg = max(1, dmg)

    target_entity["hp"] -= dmg
    print(f"[DEBUG] 扣血后 {target_entity['name']} HP = {target_entity['hp']}")

    # 检查目标是否死亡
    killed = []
    if target_entity["hp"] <= 0:
        killed.append(target_entity)

    # 发放击杀奖励（普通攻击，技能为 None）
    if killed:
        grant_kill_rewards(attacker, None, killed)

    # 消息和伤害数字
    msg = f"{attacker['name']} 攻击 {target_entity['name']}，造成 {dmg} 伤害"
    print(msg)
    game.add_battle_message(msg)

    # 添加伤害数字
    target_type = combatants[target_index]["type"]
    slot_idx = combatants[target_index]["slot_index"]
    if target_type == "player":
        pos = formation.PLAYER_POSITIONS[slot_idx]
        pos = (pos[0] + formation.SLOT_WIDTH//2, pos[1] - 20)
    else:
        pos = formation.ENEMY_POSITIONS[slot_idx]
        pos = (pos[0] + formation.SLOT_WIDTH//2, pos[1] - 20)
    game.add_damage_number(pos, dmg)

    # 攻击后嘲讽度+1
    attacker["taunt"] = attacker.get("taunt", 1) + 1
    print(f"{attacker['name']} 的嘲讽度增加到 {attacker['taunt']}")

    # 增加攻击者的疲劳
    attacker["fatigue"] = attacker.get("fatigue", 0) + 1

    result = cleanup_combatants(combatants)
    if result != "continue":
        return result, 0, skill_points

    # 重新定位攻击者索引
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

def use_skill(combatants, current_index, player_team, enemies, target_idx=None):
    """
    使用当前行动者的第一个技能。
    返回 (result, next_index, new_skill_points, need_target, skill_info)
    """
    attacker_entity = combatants[current_index]["entity"]

    # 检查技能是否存在
    skills = attacker_entity.get("skills")
    if not skills:
        print(f"{attacker_entity['name']} 没有技能！")
        return "continue", current_index, 0, False, None

    # 获取第一个技能，并确保它是字典
    skill = skills[0]
    if not isinstance(skill, dict):
        print(f"错误：{attacker_entity['name']} 的技能格式错误，应为字典")
        return "continue", current_index, 0, False, None
    
    # 技能使用奖励：+1 熟练度
    skill["proficiency"] = skill.get("proficiency", 0) + 1
    check_skill_upgrade(skill, attacker_entity)

    # 防御性检查：补全缺失的字段
    if "target" not in skill:
        print(f"警告：{attacker_entity['name']} 的技能 {skill.get('name', '未知')} 缺少 target 字段，使用默认值 'self'")
        skill["target"] = "self"
    if "type" not in skill:
        print(f"警告：{attacker_entity['name']} 的技能 {skill.get('name', '未知')} 缺少 type 字段，使用默认值 'attack'")
        skill["type"] = "attack"
    if "value" not in skill:
        print(f"警告：{attacker_entity['name']} 的技能 {skill.get('name', '未知')} 缺少 value 字段，使用默认值 0")
        skill["value"] = 0

    # 判断是否需要目标
    if skill["target"] == "self":
        # 自身技能
        if skill["type"] == "taunt":
            attacker_entity["taunt"] = attacker_entity.get("taunt", 1) + skill["value"]
            msg = f"{attacker_entity['name']} 使用 {skill['name']}，嘲讽度+{skill['value']}"  
            print(msg)                                                                        
            game.add_battle_message(msg)

        # 其他自身技能可扩展
        new_skill_points = game.current_skill_points - 1
        update_combatants(combatants, current_index)
        next_idx = get_next_attacker(combatants)
        return "continue", next_idx, new_skill_points, False, None

    elif skill["target"] == "single":
        if target_idx is None:
            return "need_target", current_index, 0, True, skill
        else:
            if skill["type"] == "heal":
                target_entity = player_team[target_idx]  # target_idx 是 player_team 索引
                heal = skill["value"]
                target_entity["hp"] = min(target_entity["max_hp"], target_entity["hp"] + heal)
                msg = f"{attacker_entity['name']} 治疗 {target_entity['name']}，恢复 {heal} HP"   
                print(msg)                                                                    
                game.add_battle_message(msg)   
                # 添加绿色数字
                pos = formation.PLAYER_POSITIONS[target_idx]  # 简化：需根据实际站位获取坐标
                pos = (pos[0] + formation.SLOT_WIDTH//2, pos[1] - 20)
                game.add_damage_number(pos, heal, color=GREEN)
            elif skill["type"] == "attack":
                target_entity = enemies[target_idx]  # target_idx 是敌人列表索引
                base_atk = attacker_entity["atk"] + skill["value"]
                factor = get_attack_factor()
                base_dmg = int(base_atk * factor)
                mult = get_attack_multiplier(attacker_entity)
                dmg = int(base_dmg * mult)
                dmg = max(1, dmg)
                target_entity["hp"] -= dmg
                msg = f"{attacker_entity['name']} 使用 {skill['name']} 攻击 {target_entity['name']}，造成 {dmg} 伤害"
                print(msg)
                game.add_battle_message(msg)

                # 添加伤害数字
                slot_idx = target_entity.get("slot", 0)
                pos = formation.ENEMY_POSITIONS[slot_idx]
                pos = (pos[0] + formation.SLOT_WIDTH//2, pos[1] - 20)
                game.add_damage_number(pos, dmg, color=RED)

                # 增加攻击者的疲劳
                attacker_entity["fatigue"] = attacker_entity.get("fatigue", 0) + 1

                # 检查战斗结果
                result = cleanup_combatants(combatants)
                if result != "continue":
                    return result, 0, 0, False, None

            # 技能消耗
            new_skill_points = game.current_skill_points - 1
            update_combatants(combatants, current_index)
            next_idx = get_next_attacker(combatants)
            return "continue", next_idx, new_skill_points, False, None

    elif skill["target"] == "all":
        if skill["type"] == "heal":
            heal = skill["value"]
            for role in player_team:
                if role["hp"] > 0:
                    role["hp"] = min(role["max_hp"], role["hp"] + heal)
            msg = f"{attacker_entity['name']} 使用 {skill['name']}，全体治疗 {heal} HP"   
            print(msg)                                                              
            game.add_battle_message(msg)               
            new_skill_points = game.current_skill_points - 1
            update_combatants(combatants, current_index)
            next_idx = get_next_attacker(combatants)
            return "continue", next_idx, new_skill_points, False, None

    return "continue", current_index, 0, False, None

def enemy_attack(combatants, attacker_index, target_index):
    """
    敌人攻击指定目标
    返回 (result, next_index)
    """
    enemy = combatants[attacker_index]["entity"]
    target_entity = combatants[target_index]["entity"]
    
    # 基础伤害 = 敌人攻击力 × 随机因子（与玩家使用相同的因子函数）
    factor = get_attack_factor()
    base_dmg = int(enemy["atk"] * factor)
    # 应用疲劳倍率（需要导入 get_attack_multiplier）
    mult = get_attack_multiplier(enemy)
    dmg = int(base_dmg * mult)
    dmg = max(1, dmg)
    target_entity["hp"] -= dmg
    print(f"[DEBUG] 扣血后 {target_entity['name']} HP = {target_entity['hp']}")   # 新增
    msg = f"{enemy['name']} 攻击 {target_entity['name']}，造成 {dmg} 伤害"   
    print(msg)                                                          
    game.add_battle_message(msg)      
    # 添加伤害数字
    target_type = combatants[target_index]["type"]
    slot_idx = combatants[target_index]["slot_index"]
    if target_type == "player":
        pos = formation.PLAYER_POSITIONS[slot_idx]
        pos = (pos[0] + formation.SLOT_WIDTH//2, pos[1] - 20)
    else:
        pos = formation.ENEMY_POSITIONS[slot_idx]
        pos = (pos[0] + formation.SLOT_WIDTH//2, pos[1] - 20)
    game.add_damage_number(pos, dmg)
    enemy["fatigue"] = enemy.get("fatigue", 0) + 1

    result = cleanup_combatants(combatants)
    if result != "continue":
        return result, 0

    # 重新定位敌人索引（可能因死亡前移）
    new_current = None
    for i, c in enumerate(combatants):
        if c["entity"] is enemy:
            new_current = i
            break
    if new_current is None:
        # 如果敌人死亡（理论上不会到这里，因为如果敌人死亡，result 应该是 "win" 或 "lose"）
        return "lose", 0

    update_combatants(combatants, new_current)
    next_index = get_next_attacker(combatants)
    return "continue", next_index

def calculate_taunt_probabilities(combatants):
    """
    计算所有存活的玩家单位的被攻击概率（基于嘲讽度）
    """
    # 找出所有存活的玩家单位
    player_indices = [i for i, c in enumerate(combatants) if c["type"] == "player" and c["entity"]["hp"] > 0]
    total_taunt = sum(combatants[i]["entity"].get("taunt", 1) for i in player_indices)
    if total_taunt == 0:
        return {i: 1/len(player_indices) for i in player_indices}
    probs = {}
    for i in player_indices:
        taunt = combatants[i]["entity"].get("taunt", 1)
        probs[i] = taunt / total_taunt
    return probs

def reset_team_hp(team):
    for role in team:
        role["hp"] = role["max_hp"]
        role["fatigue"] = 0   # 重置疲劳