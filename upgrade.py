# upgrade.py - 养成逻辑

import random
from constants import *
from config import skill_config as skill_cfg

def use_exp_book(selected_role_index, player_team, inventory):
    if inventory["exp_book"] > 0:
        role = player_team[selected_role_index]
        inventory["exp_book"] -= 1
        add_exp = 80 + random.randint(0, 40)
        role["exp"] += add_exp
        print(f"使用经验书：获得 {add_exp} 经验")
        while role["exp"] >= role["exp_to_next"]:
            role["exp"] -= role["exp_to_next"]
            role["level"] += 1
            role["exp_to_next"] = int(role["exp_to_next"] * 1.5)
            role["max_hp"] += 15
            role["hp"] = role["max_hp"]
            role["atk"] += 5
            role["stamina"] += 8
            print(f"{role['name']} 升级到 Lv.{role['level']}")

def use_skill_book(selected_role_index, player_team, inventory):
    """使用技能书，随机升级选中角色的一个技能"""
    if inventory["skill_book"] <= 0:
        print("技能书不足！")
        return

    role = player_team[selected_role_index]
    inventory["skill_book"] -= 1

    skills = role.get("skills")
    if not skills:
        print(f"{role['name']} 没有技能！")
        return

    # 随机选择一个技能升级
    skill = random.choice(skills)

    # 增加熟练度（使用配置中的范围）
    gain = skill_cfg.SKILL_PROFICIENCY_GAIN_MIN + random.randint(
        0, skill_cfg.SKILL_PROFICIENCY_GAIN_MAX - skill_cfg.SKILL_PROFICIENCY_GAIN_MIN
    )
    skill["proficiency"] += gain
    print(f"{role['name']} 的 {skill['name']} 熟练度增加 {gain}")

    # 检查是否升级
    while skill["proficiency"] >= skill["prof_to_next"]:
        skill["proficiency"] -= skill["prof_to_next"]
        skill["level"] += 1
        skill["prof_to_next"] = int(skill["prof_to_next"] * 1.6)

        # 根据技能类型应用升级效果
        skill_type = skill.get("type")
        if skill_type in ("attack", "heal"):
            # 攻击或治疗技能：效果值 + 配置值
            skill["value"] = skill.get("value", 20) + skill_cfg.ATTACK_HEAL_UPGRADE_VALUE_INCREASE
            print(f"  {skill['name']} 升级到 Lv.{skill['level']}，效果值+{skill_cfg.ATTACK_HEAL_UPGRADE_VALUE_INCREASE}，现为 {skill['value']}")
        elif skill_type == "taunt":
            # 嘲讽技能：嘲讽值增加量 + 配置值，并回复自身一定比例最大生命值
            skill["value"] = skill.get("value", 5) + skill_cfg.TAUNT_UPGRADE_VALUE_INCREASE
            heal = int(role["max_hp"] * skill_cfg.TAUNT_UPGRADE_HEAL_RATIO)
            role["hp"] = min(role["max_hp"], role["hp"] + heal)
            print(f"  {skill['name']} 升级到 Lv.{skill['level']}，嘲讽值增加量+{skill_cfg.TAUNT_UPGRADE_VALUE_INCREASE}，并回复 {heal} HP")
        else:
            # 其他类型默认增加效果值
            skill["value"] = skill.get("value", 20) + skill_cfg.DEFAULT_UPGRADE_VALUE_INCREASE
            print(f"  {skill['name']} 升级到 Lv.{skill['level']}，效果值+{skill_cfg.DEFAULT_UPGRADE_VALUE_INCREASE}")

    print(f"技能书使用完毕，剩余 {inventory['skill_book']} 本")

def toggle_active(selected_role_index, player_team):
    role = player_team[selected_role_index]
    if role.get("active", False):
        role["active"] = False
        print(f"{role['name']} 已设为待命")
    else:
        active_count = sum(1 for r in player_team if r.get("active", False))
        if active_count >= MAX_ACTIVE:
            print(f"上阵人数已达上限（最多{MAX_ACTIVE}人）")
        else:
            role["active"] = True
            print(f"{role['name']} 已设为上阵")