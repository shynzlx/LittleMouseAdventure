# formation.py - 阵型管理

# 玩家站位：三行两列，坐标 (x, y) 相对于屏幕左上角
PLAYER_POSITIONS = [
    (150, 150),   # 第1行第1列
    (400, 150),   # 第1行第2列
    (150, 280),   # 第2行第1列
    (400, 280),   # 第2行第2列
    (150, 410),   # 第3行第1列
    (400, 410)    # 第3行第2列
]

# 敌方站位：三行两列
ENEMY_POSITIONS = [
    (800, 150),   # 第1行第1列
    (1050, 150),  # 第1行第2列
    (800, 280),   # 第2行第1列
    (1050, 280),  # 第2行第2列
    (800, 410),   # 第3行第1列
    (1050, 410)   # 第3行第2列
]

# 每个站位的宽度和高度
SLOT_WIDTH = 80
SLOT_HEIGHT = 120

def get_player_slots(active_team):
    """
    根据上阵角色列表，返回玩家站位列表，每个元素为 (角色, 位置索引, 坐标)
    如果角色数少于6，则多余位置为 None
    """
    slots = []
    for i, pos in enumerate(PLAYER_POSITIONS):
        if i < len(active_team):
            slots.append((active_team[i], i, pos))
        else:
            slots.append((None, i, pos))
    return slots

def get_enemy_slots(enemy):
    """
    敌方目前只有一个敌人，但为了阵型统一，也返回列表
    enemy 是单个敌人字典，放在第一个位置，其余为空
    """
    slots = []
    for i, pos in enumerate(ENEMY_POSITIONS):
        if i == 0:
            slots.append((enemy, i, pos))
        else:
            slots.append((None, i, pos))
    return slots