# battle.py - 战斗逻辑

import random
from constants import *

def player_attack(player_team, enemy, game_state, battle_turn):
    """玩家攻击（仅存活角色参与）"""
    print("player_attack 被调用")
    # 筛选存活角色
    alive_team = [r for r in player_team if r["hp"] > 0]
    if not alive_team:
        # 没有存活角色时无法攻击（理论上不会发生，因为攻击按钮应在有存活时才能点）
        print("没有存活角色，无法攻击")
        return game_state, battle_turn
    dmg = random.randint(20, 40) + (sum(r["atk"] for r in alive_team) // len(alive_team))
    enemy["hp"] -= dmg
    print(f"攻击！造成 {dmg} 伤害，敌人剩余 HP: {enemy['hp']}")
    if enemy["hp"] <= 0:
        print("胜利！")
        game_state = STATE_CHALLENGE
    else:
        battle_turn = "enemy"
    return game_state, battle_turn

def player_skill(player_team, game_state, battle_turn):
    """玩家技能（治疗存活角色）"""
    print("player_skill 被调用")
    heal = random.randint(20, 35)
    for role in player_team:
        if role["hp"] > 0:  # 只治疗活着的角色
            role["hp"] = min(role["max_hp"], role["hp"] + heal)
    print(f"全体治疗 {heal} HP")
    battle_turn = "enemy"
    return game_state, battle_turn

def enemy_attack(player_team, enemy, game_state, battle_turn):
    """敌人攻击"""
    print("enemy_attack 被调用")
    if not player_team:
        return game_state, battle_turn
    # 只选择活着的角色
    alive_team = [r for r in player_team if r["hp"] > 0]
    if not alive_team:
        print("队伍全灭！")
        game_state = STATE_CHALLENGE
        battle_turn = "player"
        return game_state, battle_turn
    target = random.choice(alive_team)
    dmg = random.randint(15, 30)
    target["hp"] -= dmg
    print(f"{enemy['name']} 攻击 {target['name']}，造成 {dmg} 伤害")
    if all(r["hp"] <= 0 for r in player_team):
        print("失败！队伍全灭")
        game_state = STATE_CHALLENGE
    battle_turn = "player"
    return game_state, battle_turn
