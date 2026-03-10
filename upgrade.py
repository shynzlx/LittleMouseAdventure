# upgrade.py - 养成逻辑

import random
from constants import *

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
    if inventory["skill_book"] > 0:
        role = player_team[selected_role_index]
        inventory["skill_book"] -= 1
        if len(role["skills"]) < 4:
            new_skill = {"name": f"技能{len(role['skills'])+1}", "level": 1, "proficiency": 0, "prof_to_next": 50}
            role["skills"].append(new_skill)
            print(f"{role['name']} 学会新技能：{new_skill['name']}")
        else:
            sk = random.choice(role["skills"])
            sk["proficiency"] += 30 + random.randint(0, 20)
            if sk["proficiency"] >= sk["prof_to_next"]:
                sk["level"] += 1
                sk["proficiency"] = 0
                sk["prof_to_next"] = int(sk["prof_to_next"] * 1.6)
                print(f"技能 {sk['name']} 升级到 Lv.{sk['level']}")
from constants import MAX_ACTIVE   # 导入常量

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