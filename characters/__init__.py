import os
import importlib.util

def load_friendly_roles():
    """加载 friendly 文件夹中的所有角色（返回 ROLE_DATA 字典列表）"""
    roles = []
    folder = os.path.join(os.path.dirname(__file__), "friendly")
    for filename in os.listdir(folder):
        if filename.endswith(".py") and not filename.startswith("__"):
            file_path = os.path.join(folder, filename)
            spec = importlib.util.spec_from_file_location(filename[:-3], file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "ROLE_DATA"):
                roles.append(module.ROLE_DATA)
    return roles

def load_all_roles():
    """供旧代码调用，返回所有友方角色"""
    return load_friendly_roles()

def load_enemy_base(enemy_name):
    """根据名称加载敌人基础数据"""
    folder = os.path.join(os.path.dirname(__file__), "enemy")
    for filename in os.listdir(folder):
        if filename.endswith(".py") and not filename.startswith("__"):
            file_path = os.path.join(folder, filename)
            spec = importlib.util.spec_from_file_location(filename[:-3], file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "name") and module.name == enemy_name:
                return {
                    "name": module.name,
                    "base_stats": module.base_stats,
                    "growth": module.growth,
                    "skills": getattr(module, "skills", [])
                }
    return None