# avatar_mapper.py
# 角色头像映射（硬编码）
# 键为角色名称（字符串），值为头像文件名（相对于 assets/avatars/ 目录）

AVATAR_MAP = {
    "一般鼠鼠": "mouse_common.png",
    "稀有鼠鼠": "mouse_rare.png",
    "盾牌鼠鼠": "mouse_shield.png",
    "传奇鼠鼠": "mouse_legend.png",
}

# 新增进攻头像映射，键为角色名，值为进攻头像文件名
ATTACK_AVATAR_MAP = {
    "一般鼠鼠": "mouse_common_attack.png",
    "稀有鼠鼠": "mouse_rare_attack.png",
    "盾牌鼠鼠": "mouse_shield_attack.png",
    "传奇鼠鼠": "mouse_legend_attack.png",
}

def get_avatar_filename(role_name):
    return AVATAR_MAP.get(role_name)

def get_attack_avatar_filename(role_name):
    """根据角色名称返回进攻头像文件名"""
    return ATTACK_AVATAR_MAP.get(role_name)