"""
邮箱和文件验证工具
"""
import re
import os


def validate_email(email: str) -> bool:
    """验证邮箱地址格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))


def validate_file(filepath: str, extensions: list = None) -> tuple[bool, str]:
    """
    验证文件是否存在且格式正确
    
    Args:
        filepath: 文件路径
        extensions: 允许的扩展名列表，如 ['.txt', '.csv']
    
    Returns:
        (是否有效, 错误信息)
    """
    if not filepath:
        return False, "文件路径为空"
    
    if not os.path.exists(filepath):
        return False, f"文件不存在: {filepath}"
    
    if not os.path.isfile(filepath):
        return False, f"不是文件: {filepath}"
    
    if extensions:
        ext = os.path.splitext(filepath)[1].lower()
        if ext not in extensions:
            return False, f"不支持的文件格式: {ext}，支持: {', '.join(extensions)}"
    
    return True, ""
