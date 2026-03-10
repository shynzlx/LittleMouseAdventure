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
    (800, 150),   # 站位0
    (1050, 150),  # 站位1
    (800, 280),   # 站位2
    (1050, 280),  # 站位3
    (800, 410),   # 站位4
    (1050, 410)   # 站位5
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

def get_enemy_slots(enemies):
    """
    根据敌人列表中的 slot 字段，返回每个站位对应的敌人。
    返回列表，每个元素为 (敌人, 站位索引, 坐标)
    """
    # 初始化所有站位为 None
    slots = [None] * len(ENEMY_POSITIONS)

    for enemy in enemies:
        slot_idx = enemy.get("slot")
        if slot_idx is not None and 0 <= slot_idx < len(slots):
            # 如果指定站位已被占用，打印警告并跳过（或覆盖？这里选择覆盖）
            if slots[slot_idx] is not None:
                print(f"警告：站位 {slot_idx} 已被 {slots[slot_idx]['name']} 占用，{enemy['name']} 将覆盖")
            slots[slot_idx] = enemy
        else:
            # 没有指定 slot 或无效，则按顺序分配到第一个空闲站位
            assigned = False
            for i in range(len(slots)):
                if slots[i] is None:
                    slots[i] = enemy
                    assigned = True
                    break
            if not assigned:
                print(f"错误：没有空闲站位给敌人 {enemy['name']}，已忽略")

    # 转换为带坐标的列表
    result = []
    for i, enemy in enumerate(slots):
        result.append((enemy, i, ENEMY_POSITIONS[i]))
    return result