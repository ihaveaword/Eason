"""核心业务逻辑模块"""
from .email_sender import EmailSender
from .contact_fetcher import ContactFetcher
from .config_manager import ConfigManager
from .email_config import get_email_config, get_smtp_server, get_imap_server, get_supported_domains
from .contact_db import ContactDatabase

__all__ = [
    'EmailSender', 
    'ContactFetcher', 
    'ConfigManager',
    'ContactDatabase',
    'get_email_config',
    'get_smtp_server',
    'get_imap_server',
    'get_supported_domains',
]
