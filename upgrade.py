# upgrade.py - 养成逻辑

import random
import math
from constants import *
from config import skill_config as skill_cfg
from config import level_config as level_cfg

def use_exp_book(selected_role_index, player_team, inventory):
    if inventory["exp_book"] > 0:
        role = player_team[selected_role_index]
        inventory["exp_book"] -= 1
        add_exp = level_cfg.EXP_BOOK_GAIN_MIN + random.randint(0, level_cfg.EXP_BOOK_GAIN_MAX - level_cfg.EXP_BOOK_GAIN_MIN)
        role["exp"] += add_exp
        print(f"使用经验书：获得 {add_exp} 经验")
        while role["exp"] >= role["exp_to_next"]:
            role["exp"] -= role["exp_to_next"]
            role["level"] += 1
            # 直接按公式计算下一级所需经验（避免累积误差）
            new_level = role["level"] + 1  # 下一级的等级
            role["exp_to_next"] = int(round(
                level_cfg.BASE_EXP_TO_NEXT * (level_cfg.NEXT_LEVEL_EXP_FACTOR ** (new_level - 1))
            ))
            # 属性增加
            role["max_hp"] += level_cfg.LEVEL_UP_HP_INCREASE
            role["hp"] = role["max_hp"]
            role["atk"] += level_cfg.LEVEL_UP_ATK_INCREASE
            role["stamina"] += level_cfg.LEVEL_UP_STAMINA_INCREASE
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
        old_level = skill["level"]
        skill["level"] += 1
        new_level = skill["level"]
        skill["prof_to_next"] = int(skill["prof_to_next"] * 1.6)

        # 获取技能类型，选择增量公式
        skill_type = skill.get("type", "default")
        formula = skill_cfg.INCREMENT_FORMULAS.get(skill_type)

        # 准备命名空间（提供当前等级和 math 模块）
        namespace = {"level": old_level, "math": math}
        try:
            increment = eval(formula, {"__builtins__": {}}, namespace)
        except Exception as e:
            print(f"技能增量公式计算错误: {e}，使用默认增量 0")
            increment = 0

        # 确保数值类型
        if not isinstance(increment, (int, float)):
            increment = 0

        # 更新技能效果值
        old_value = skill.get("value", 0)
        skill["value"] = old_value + increment

        # 嘲讽技能特殊效果：回血
        if skill_type == "taunt":
            heal = int(role["max_hp"] * skill_cfg.TAUNT_UPGRADE_HEAL_RATIO)
            role["hp"] = min(role["max_hp"], role["hp"] + heal)
            print(f"  {skill['name']} 升级到 Lv.{new_level}，效果值 +{increment:.2f}（现 {skill['value']:.2f}），并回复 {heal} HP")
        else:
            print(f"  {skill['name']} 升级到 Lv.{new_level}，效果值 +{increment:.2f}，现为 {skill['value']:.2f}")

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