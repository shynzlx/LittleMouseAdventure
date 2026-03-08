# battle.py - 战斗逻辑

import random
from constants import *

def player_attack(player_team, enemy, game_state, battle_turn):
    """玩家攻击"""
    print("player_attack 被调用")  # 调试输出
    dmg = random.randint(20, 40) + (sum(r["atk"] for r in player_team) // len(player_team) if player_team else 0)
    enemy["hp"] -= dmg
    print(f"攻击！造成 {dmg} 伤害，敌人剩余 HP: {enemy['hp']}")
    if enemy["hp"] <= 0:
        print("胜利！")
        game_state = STATE_CHALLENGE
    else:
        battle_turn = "enemy"
    return game_state, battle_turn

def player_skill(player_team, game_state, battle_turn):
    """玩家技能（治疗）"""
    print("player_skill 被调用")
    heal = random.randint(20, 35)
    for role in player_team:
        role["hp"] = min(role["max_hp"], role["hp"] + heal)
    print(f"全体治疗 {heal} HP")
    battle_turn = "enemy"
    return game_state, battle_turn

def enemy_attack(player_team, enemy, game_state, battle_turn):
    """敌人攻击"""
    print("enemy_attack 被调用")
    if not player_team:
        return game_state, battle_turn
    target = random.choice(player_team)
    dmg = random.randint(15, 30)
    target["hp"] -= dmg
    print(f"{enemy['name']} 攻击 {target['name']}，造成 {dmg} 伤害")
    if all(r["hp"] <= 0 for r in player_team):
        print("失败！队伍全灭")
        game_state = STATE_CHALLENGE
    battle_turn = "player"
    return game_state, battle_turn