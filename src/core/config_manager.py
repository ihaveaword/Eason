"""
配置管理器
使用 macOS NSUserDefaults 存储配置
支持HTML模板配置
"""
import json
from PyQt6.QtCore import QSettings


class ConfigManager:
    """应用配置管理"""
    
    def __init__(self):
        self.settings = QSettings('com.EmailAssistant', 'BatchSender')
    
    def save_email_config(self, username: str, password: str):
        """保存邮箱配置"""
        self.settings.setValue('username', username)
        # TODO: 加密存储密码
        self.settings.setValue('password', password)
    
    def load_email_config(self) -> tuple[str, str]:
        """加载邮箱配置"""
        username = self.settings.value('username', '')
        password = self.settings.value('password', '')
        return username, password
    
    def save_send_config(self, subject: str, body: str, batch_size: int, interval: int):
        """保存发送配置"""
        self.settings.setValue('subject', subject)
        self.settings.setValue('body', body)
        self.settings.setValue('batch_size', batch_size)
        self.settings.setValue('interval', interval)
    
    def load_send_config(self) -> dict:
        """加载发送配置"""
        return {
            'subject': self.settings.value('subject', ''),
            'body': self.settings.value('body', ''),
            'batch_size': int(self.settings.value('batch_size', 10)),
            'interval': int(self.settings.value('interval', 30))
        }
    
    def save_fetch_config(self, limit: int):
        """保存采集配置"""
        self.settings.setValue('fetch_limit', limit)
    
    def load_fetch_config(self) -> int:
        """加载采集配置"""
        return int(self.settings.value('fetch_limit', 200))
    
    def save_last_contact_file(self, filepath: str):
        """保存最后使用的联系人文件路径"""
        self.settings.setValue('last_contact_file', filepath)
    
    def load_last_contact_file(self) -> str:
        """加载最后使用的联系人文件路径"""
        return self.settings.value('last_contact_file', '')
    
    def clear_all(self):
        """清空所有配置"""
        self.settings.clear()
    
    def save_template_config(self, template_name: str, variables: dict, enabled: bool = True):
        """保存模板配置"""
        self.settings.setValue('template/name', template_name)
        self.settings.setValue('template/variables', json.dumps(variables))
        self.settings.setValue('template/enabled', enabled)
    
    def load_template_config(self) -> dict:
        """加载模板配置"""
        variables_json = self.settings.value('template/variables', '{}')
        try:
            variables = json.loads(variables_json)
        except Exception:
            variables = {}
        
        return {
            'template_name': self.settings.value('template/name', ''),
            'variables': variables,
            'enabled': self.settings.value('template/enabled', False, type=bool)
        }
