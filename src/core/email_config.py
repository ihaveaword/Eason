"""
邮箱服务器配置
自动根据邮箱后缀识别 SMTP/IMAP 服务器
"""

# 常见邮箱服务器配置
EMAIL_SERVERS = {
    # 网易邮箱
    '163.com': {
        'smtp': 'smtp.163.com',
        'imap': 'imap.163.com',
        'smtp_port': 465,
        'imap_port': 993,
    },
    '126.com': {
        'smtp': 'smtp.126.com',
        'imap': 'imap.126.com',
        'smtp_port': 465,
        'imap_port': 993,
    },
    'yeah.net': {
        'smtp': 'smtp.yeah.net',
        'imap': 'imap.yeah.net',
        'smtp_port': 465,
        'imap_port': 993,
    },
    # QQ邮箱
    'qq.com': {
        'smtp': 'smtp.qq.com',
        'imap': 'imap.qq.com',
        'smtp_port': 465,
        'imap_port': 993,
    },
    'foxmail.com': {
        'smtp': 'smtp.qq.com',
        'imap': 'imap.qq.com',
        'smtp_port': 465,
        'imap_port': 993,
    },
    # 阿里邮箱
    'aliyun.com': {
        'smtp': 'smtp.aliyun.com',
        'imap': 'imap.aliyun.com',
        'smtp_port': 465,
        'imap_port': 993,
    },
    # 新浪邮箱
    'sina.com': {
        'smtp': 'smtp.sina.com',
        'imap': 'imap.sina.com',
        'smtp_port': 465,
        'imap_port': 993,
    },
    # Gmail
    'gmail.com': {
        'smtp': 'smtp.gmail.com',
        'imap': 'imap.gmail.com',
        'smtp_port': 465,
        'imap_port': 993,
    },
    # Outlook / Hotmail
    'outlook.com': {
        'smtp': 'smtp-mail.outlook.com',
        'imap': 'outlook.office365.com',
        'smtp_port': 587,  # Outlook 使用 STARTTLS
        'imap_port': 993,
        'use_tls': True,  # 使用 STARTTLS 而非 SSL
    },
    'hotmail.com': {
        'smtp': 'smtp-mail.outlook.com',
        'imap': 'outlook.office365.com',
        'smtp_port': 587,
        'imap_port': 993,
        'use_tls': True,
    },
    'live.com': {
        'smtp': 'smtp-mail.outlook.com',
        'imap': 'outlook.office365.com',
        'smtp_port': 587,
        'imap_port': 993,
        'use_tls': True,
    },
}

# 默认配置（163邮箱）- 确保向后兼容
DEFAULT_CONFIG = {
    'smtp': 'smtp.163.com',
    'imap': 'imap.163.com',
    'smtp_port': 465,
    'imap_port': 993,
}


def get_email_domain(email: str) -> str:
    """从邮箱地址提取域名"""
    if '@' in email:
        return email.split('@')[1].lower()
    return ''


def get_email_config(email: str) -> dict:
    """
    根据邮箱地址获取服务器配置
    
    Args:
        email: 邮箱地址，如 user@163.com
        
    Returns:
        包含 smtp, imap, smtp_port, imap_port 的配置字典
    """
    domain = get_email_domain(email)
    
    if domain in EMAIL_SERVERS:
        return EMAIL_SERVERS[domain]
    
    # 未识别的邮箱，返回默认配置（163）
    return DEFAULT_CONFIG


def get_smtp_server(email: str) -> str:
    """获取 SMTP 服务器地址"""
    config = get_email_config(email)
    return config['smtp']


def get_imap_server(email: str) -> str:
    """获取 IMAP 服务器地址"""
    config = get_email_config(email)
    return config['imap']


def get_smtp_port(email: str) -> int:
    """获取 SMTP 端口"""
    config = get_email_config(email)
    return config.get('smtp_port', 465)


def get_imap_port(email: str) -> int:
    """获取 IMAP 端口"""
    config = get_email_config(email)
    return config.get('imap_port', 993)


def use_starttls(email: str) -> bool:
    """是否使用 STARTTLS（而非 SSL）"""
    config = get_email_config(email)
    return config.get('use_tls', False)


def get_supported_domains() -> list:
    """获取支持的邮箱域名列表"""
    return list(EMAIL_SERVERS.keys())
