"""
联系人采集模块
从邮箱收件箱采集发件人地址
支持多种邮箱：163、126、QQ、Gmail、Outlook 等
支持多种采集来源、过滤器、信息增强
"""
import time
import imaplib
import re
from datetime import datetime, timedelta
from email import message_from_bytes
from email.utils import parseaddr, parsedate_to_datetime
from email.header import decode_header
from typing import List, Dict, Optional
from collections import Counter
from PyQt6.QtCore import QThread, pyqtSignal
from .email_config import get_imap_server, get_imap_port


class ContactInfo:
    """联系人信息"""
    def __init__(self, email: str, name: str = ""):
        self.email = email.lower()
        self.name = name
        self.count = 1  # 出现次数
        self.last_contact = None  # 最后联系时间
        self.first_contact = None  # 首次联系时间
    
    def update(self, name: str = "", contact_time: datetime = None):
        """更新联系人信息"""
        self.count += 1
        if name and not self.name:
            self.name = name
        if contact_time:
            if self.last_contact is None or contact_time > self.last_contact:
                self.last_contact = contact_time
            if self.first_contact is None or contact_time < self.first_contact:
                self.first_contact = contact_time
    
    def to_dict(self) -> dict:
        return {
            'email': self.email,
            'name': self.name,
            'count': self.count,
            'last_contact': self.last_contact.strftime('%Y-%m-%d %H:%M') if self.last_contact else '',
            'first_contact': self.first_contact.strftime('%Y-%m-%d %H:%M') if self.first_contact else '',
        }


class ContactFetcher(QThread):
    """联系人采集线程 - 增强版"""
    
    # 信号
    progress = pyqtSignal(int, str)  # 进度, 当前邮箱
    result = pyqtSignal(str)  # 日志消息
    error = pyqtSignal(str)  # 错误消息
    finished = pyqtSignal()  # 完成
    stats = pyqtSignal(dict)  # 统计数据
    contacts_ready = pyqtSignal(list)  # 联系人列表（ContactInfo）
    
    # 文件夹映射
    FOLDER_MAP = {
        'inbox': 'INBOX',
        'sent': 'Sent Messages',  # 163
        'sent_qq': 'Sent',  # QQ
        'sent_gmail': '[Gmail]/Sent Mail',
        'all': None,  # 所有文件夹
    }
    
    def __init__(self, username: str, password: str, limit: int = 200, 
                 imap_server: str = None, options: dict = None):
        super().__init__()
        self.username = username
        self.password = password
        self.limit = limit
        
        # 自动检测邮箱服务器
        if imap_server:
            self.imap_server = imap_server
            self.imap_port = 993
        else:
            self.imap_server = get_imap_server(username)
            self.imap_port = get_imap_port(username)
        
        # 采集选项
        self.options = options or {}
        self.folder = self.options.get('folder', 'inbox')
        self.date_range = self.options.get('date_range', 'all')  # all, 7, 30, 90, custom
        self.date_from = self.options.get('date_from')
        self.date_to = self.options.get('date_to')
        self.include_domains = self.options.get('include_domains', [])  # 只包含这些域名
        self.exclude_domains = self.options.get('exclude_domains', [])  # 排除这些域名
        
        self.is_running = True
        self.contacts: Dict[str, ContactInfo] = {}
    
    def stop(self):
        """停止采集"""
        self.is_running = False
    
    def _decode_header_value(self, value: str) -> str:
        """解码邮件头"""
        if not value:
            return ""
        try:
            decoded_parts = decode_header(value)
            result = []
            for part, charset in decoded_parts:
                if isinstance(part, bytes):
                    result.append(part.decode(charset or 'utf-8', errors='ignore'))
                else:
                    result.append(part)
            return ''.join(result)
        except:
            return value
    
    def _get_date_criteria(self) -> str:
        """生成日期搜索条件"""
        if self.date_range == 'all':
            return None
        
        if self.date_range == 'custom':
            if self.date_from:
                return f'SINCE {self.date_from.strftime("%d-%b-%Y")}'
            return None
        
        # 最近 N 天
        days = int(self.date_range)
        since_date = datetime.now() - timedelta(days=days)
        return f'SINCE {since_date.strftime("%d-%b-%Y")}'
    
    def _filter_email(self, email: str) -> bool:
        """检查邮箱是否符合过滤条件"""
        if not email or '@' not in email:
            return False
        
        domain = email.split('@')[1].lower()
        
        # 排除系统邮件
        system_domains = ['mailer-daemon', 'postmaster', 'noreply', 'no-reply']
        if any(sd in email.lower() for sd in system_domains):
            return False
        
        # 包含域名过滤
        if self.include_domains:
            if not any(domain.endswith(d.lower()) for d in self.include_domains):
                return False
        
        # 排除域名过滤
        if self.exclude_domains:
            if any(domain.endswith(d.lower()) for d in self.exclude_domains):
                return False
        
        return True
    
    def _get_folders(self, mail) -> List[str]:
        """获取要扫描的文件夹列表"""
        if self.folder == 'all':
            # 获取所有文件夹
            status, folders = mail.list()
            if status == 'OK':
                folder_list = []
                for f in folders:
                    # 解析文件夹名称
                    match = re.search(r'"([^"]+)"$|(\S+)$', f.decode())
                    if match:
                        folder_name = match.group(1) or match.group(2)
                        folder_list.append(folder_name)
                return folder_list
            return ['INBOX']
        
        # 单个文件夹
        folder_name = self.FOLDER_MAP.get(self.folder, 'INBOX')
        
        # 根据邮箱类型调整已发送文件夹名称
        if self.folder == 'sent':
            if 'qq.com' in self.username:
                folder_name = 'Sent'
            elif 'gmail.com' in self.username:
                folder_name = '[Gmail]/Sent Mail'
            elif 'outlook.com' in self.username or 'hotmail.com' in self.username:
                folder_name = 'Sent'
            else:
                folder_name = 'Sent Messages'  # 163 默认
        
        return [folder_name]
    
    def run(self):
        """执行采集任务"""
        try:
            self.result.emit(f"🔌 正在连接 IMAP 服务器 ({self.imap_server})...")
            
            # 添加 ID 命令支持
            imaplib.Commands = {**imaplib.Commands, 'ID': ('NONAUTH',)}
            
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            
            # 发送 ID 命令
            try:
                args = b'("name" "Eason" "version" "2.0")'
                mail._simple_command('ID', args)
            except:
                pass
            
            self.result.emit("🔐 正在登录...")
            mail.login(self.username, self.password)
            time.sleep(0.5)
            
            # 获取要扫描的文件夹
            folders = self._get_folders(mail)
            self.result.emit(f"📁 将扫描 {len(folders)} 个文件夹: {', '.join(folders[:3])}{'...' if len(folders) > 3 else ''}")
            
            total_scanned = 0
            
            for folder in folders:
                if not self.is_running:
                    break
                
                try:
                    # 选择文件夹
                    status, _ = mail.select(f'"{folder}"', readonly=True)
                    if status != 'OK':
                        continue
                    
                    self.result.emit(f"📂 正在扫描: {folder}")
                    
                    # 构建搜索条件
                    search_criteria = 'ALL'
                    date_criteria = self._get_date_criteria()
                    if date_criteria:
                        search_criteria = date_criteria
                    
                    status, messages = mail.search(None, search_criteria)
                    if status != 'OK':
                        continue
                    
                    msg_ids = messages[0].split()
                    folder_total = len(msg_ids)
                    fetch_count = min(folder_total, self.limit - total_scanned)
                    
                    if fetch_count <= 0:
                        break
                    
                    self.result.emit(f"  └─ 找到 {folder_total} 封邮件，将采集 {fetch_count} 封")
                    
                    # 倒序遍历（最新的先）
                    for i in range(folder_total - 1, max(folder_total - fetch_count - 1, -1), -1):
                        if not self.is_running:
                            break
                        
                        msg_id = msg_ids[i]
                        
                        try:
                            # 获取邮件头
                            typ, msg_data = mail.fetch(msg_id, '(BODY.PEEK[HEADER.FIELDS (FROM DATE)])')
                            
                            if typ == "OK" and msg_data and msg_data[0]:
                                raw_header = msg_data[0][1]
                                msg = message_from_bytes(raw_header)
                                
                                # 解析发件人
                                from_header = self._decode_header_value(str(msg.get('From', '')))
                                name, addr = parseaddr(from_header)
                                name = self._decode_header_value(name)
                                
                                if addr and self._filter_email(addr):
                                    addr = addr.lower()
                                    
                                    # 解析日期
                                    date_str = msg.get('Date', '')
                                    contact_time = None
                                    try:
                                        contact_time = parsedate_to_datetime(date_str)
                                    except:
                                        pass
                                    
                                    # 更新联系人信息
                                    if addr in self.contacts:
                                        self.contacts[addr].update(name, contact_time)
                                    else:
                                        info = ContactInfo(addr, name)
                                        info.last_contact = contact_time
                                        info.first_contact = contact_time
                                        self.contacts[addr] = info
                                    
                                    total_scanned += 1
                                    
                                    if total_scanned % 20 == 0:
                                        self.progress.emit(total_scanned, addr)
                                        self.result.emit(f"  📧 已扫描 {total_scanned} 封，发现 {len(self.contacts)} 个联系人")
                        
                        except Exception as e:
                            continue
                        
                        if total_scanned >= self.limit:
                            break
                    
                except Exception as e:
                    self.result.emit(f"  ⚠️ 文件夹 {folder} 扫描出错: {str(e)[:50]}")
                    continue
            
            mail.close()
            mail.logout()
            
            # 生成统计数据
            stats = self._generate_stats()
            self.stats.emit(stats)
            
            # 转换为列表并排序（按出现次数）
            contact_list = sorted(self.contacts.values(), key=lambda x: x.count, reverse=True)
            self.contacts_ready.emit([c.to_dict() for c in contact_list])
            
            self.result.emit(f"✅ 采集完成！共扫描 {total_scanned} 封邮件，发现 {len(self.contacts)} 个独立联系人")
            self.finished.emit()
        
        except Exception as e:
            self.error.emit(f"采集失败: {str(e)}")
            self.finished.emit()
    
    def _generate_stats(self) -> dict:
        """生成统计数据"""
        domain_counter = Counter()
        total_interactions = 0
        
        for contact in self.contacts.values():
            domain = contact.email.split('@')[1] if '@' in contact.email else 'unknown'
            domain_counter[domain] += 1
            total_interactions += contact.count
        
        # 取前10个域名
        top_domains = domain_counter.most_common(10)
        
        return {
            'total_contacts': len(self.contacts),
            'total_interactions': total_interactions,
            'domain_distribution': dict(top_domains),
            'avg_interactions': round(total_interactions / len(self.contacts), 1) if self.contacts else 0,
        }
