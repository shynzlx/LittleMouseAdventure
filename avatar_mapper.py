# avatar_mapper.py

AVATAR_MAP = {
    "警卫鼠鼠": "guard_mouse.png",
    "短剑鼠鼠": "sword_mouse.png",
    "盾牌鼠鼠": "shield_mouse.png",
    "传奇鼠鼠": "legend_mouse.png",
}

ATTACK_AVATAR_MAP = {
    "警卫鼠鼠": "guard_mouse_attack.png",
    "短剑鼠鼠": "sword_mouse_attack.png",
    "盾牌鼠鼠": "shield_mouse_attack.png",
    "传奇鼠鼠": "legend_mouse_attack.png",
}

# 新增敌人头像映射（普通状态）
ENEMY_AVATAR_MAP = {
    "史莱姆": "enemy/slime.png",
    "哥布林": "enemy/goblin.png",
   # "哥布林弓箭手": "goblin_archer.png",
   # "哥布林首领": "goblin_chief.png",
    #"龙仔": "dragon_hatchling.png",
    #"龙王": "dragon_king.png",
}

# 新增敌人进攻头像映射（可选，如果敌人也有攻击动画）
ENEMY_ATTACK_AVATAR_MAP = {
    "史莱姆": "enemy/slime_attack.png",
    "哥布林": "enemy/goblin_attack.png"
}

def get_avatar_filename(entity_name):
    """通用获取头像文件名，先查角色，再查敌人"""
    # 先查角色
    filename = AVATAR_MAP.get(entity_name)
    if filename:
        return filename
    # 再查敌人
    return ENEMY_AVATAR_MAP.get(entity_name)

def get_attack_avatar_filename(entity_name):
    """通用获取进攻头像文件名，先查角色，再查敌人"""
    filename = ATTACK_AVATAR_MAP.get(entity_name)
    if filename:
        return filename
    return ENEMY_ATTACK_AVATAR_MAP.get(entity_name)