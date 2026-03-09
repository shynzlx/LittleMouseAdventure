# characters/__init__.py
import os
import importlib

def load_all_roles():
    """加载 characters 目录下所有角色数据，返回角色字典列表"""
    roles = []
    package_dir = os.path.dirname(__file__)          # 获取当前目录路径
    for filename in os.listdir(package_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]               # 去掉 .py 后缀
            module = importlib.import_module(f"characters.{module_name}")
            if hasattr(module, "ROLE_DATA"):
                role_data = module.ROLE_DATA.copy()   # 复制一份，避免后续意外修改
                roles.append(role_data)
    return roles