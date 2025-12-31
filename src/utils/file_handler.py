"""
联系人文件读写处理
"""
import csv
import os
from typing import List
from .validators import validate_email


def read_contacts(filepath: str) -> List[str]:
    """
    从文件读取联系人列表
    支持 .txt 和 .csv 格式
    
    Returns:
        邮箱地址列表
    """
    contacts = []
    ext = os.path.splitext(filepath)[1].lower()
    
    try:
        if ext == '.txt':
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    email = line.strip()
                    if email and validate_email(email):
                        contacts.append(email)
        
        elif ext == '.csv':
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        email = row[0].strip()
                        if email and validate_email(email):
                            contacts.append(email)
        
        else:
            raise ValueError(f"不支持的文件格式: {ext}")
    
    except Exception as e:
        raise Exception(f"读取联系人文件失败: {str(e)}")
    
    return contacts


def export_contacts(contacts: List[str], filepath: str, format_type: str = 'txt') -> bool:
    """
    导出联系人到文件
    
    Args:
        contacts: 联系人列表
        filepath: 保存路径
        format_type: 格式类型 ('txt' 或 'csv')
    
    Returns:
        是否成功
    """
    try:
        if format_type == 'txt':
            with open(filepath, 'w', encoding='utf-8') as f:
                for email in contacts:
                    f.write(f"{email}\n")
        
        elif format_type == 'csv':
            with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Email'])  # 表头
                for email in contacts:
                    writer.writerow([email])
        
        else:
            raise ValueError(f"不支持的格式: {format_type}")
        
        return True
    
    except Exception as e:
        raise Exception(f"导出联系人失败: {str(e)}")
