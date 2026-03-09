# avatar_mapper.py
# 角色头像映射（硬编码）
# 键为角色名称（字符串），值为头像文件名（相对于 assets/avatars/ 目录）
AVATAR_MAP = {
    "一般鼠鼠": "mouse_common.png",
    "稀有鼠鼠": "mouse_rare.png",
    "盾牌鼠鼠": "mouse_shield.png",
    "传奇鼠鼠": "mouse_legend.png",
    # 继续添加其他角色...
}

def get_avatar_filename(role_name):
    """根据角色名称返回对应的头像文件名，没有则返回 None"""
    return AVATAR_MAP.get(role_name)