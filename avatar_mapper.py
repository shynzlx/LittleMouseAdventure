# avatar_mapper.py
# 角色头像映射（硬编码）
# 键为角色名称（字符串），值为头像文件名（相对于 assets/avatars/ 目录）

AVATAR_MAP = {
    "警卫鼠鼠": "guard_mouse.png",
    "短剑鼠鼠": "sword_mouse.png",
    "盾牌鼠鼠": "shield_mouse.png",
    "传奇鼠鼠": "legend_mouse.png",
}

# 新增进攻头像映射，键为角色名，值为进攻头像文件名
ATTACK_AVATAR_MAP = {
    "警卫鼠鼠": "guard_mouse_attack.png",
    "短剑鼠鼠": "sword_mouse_attack.png",
    "盾牌鼠鼠": "shield_mouse_attack.png",
    "传奇鼠鼠": "legend_mouse_attack.png",
}

def get_avatar_filename(role_name):
    return AVATAR_MAP.get(role_name)

def get_attack_avatar_filename(role_name):
    """根据角色名称返回进攻头像文件名"""
    return ATTACK_AVATAR_MAP.get(role_name)