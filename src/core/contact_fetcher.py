"""
联系人采集模块
从邮箱收件箱采集发件人地址
"""
import time
import imaplib
from email import message_from_bytes
from email.utils import parseaddr
from PyQt6.QtCore import QThread, pyqtSignal


class ContactFetcher(QThread):
    """联系人采集线程"""
    
    log_signal = pyqtSignal(str)
    finish_signal = pyqtSignal(list)
    error_signal = pyqtSignal(str)
    
    def __init__(self, username: str, password: str, limit: int, imap_server: str = 'imap.163.com'):
        super().__init__()
        self.username = username
        self.password = password
        self.limit = limit
        self.imap_server = imap_server
        self.is_running = True
    
    def stop(self):
        """停止采集"""
        self.is_running = False
    
    def run(self):
        """执行采集任务"""
        try:
            self.log_signal.emit(f"🔌 正在连接 IMAP 服务器 ({self.imap_server})...")
            
            # 添加 ID 命令支持
            imaplib.Commands = {**imaplib.Commands, 'ID': ('NONAUTH',)}
            
            mail = imaplib.IMAP4_SSL(self.imap_server, 993)
            
            # 发送 ID 命令（某些服务器需要）
            args = (
                b'("name" "EmailAssistant" "version" "2.0.0" '
                b'"vendor" "EmailAssistant" "support-email" "support@example.com")'
            )
            try:
                typ, data = mail._simple_command('ID', args)
                if typ != 'OK':
                    self.log_signal.emit("⚠️ 服务器未接受 ID 参数（可忽略）")
            except:
                pass
            
            self.log_signal.emit("🔐 正在登录...")
            mail.login(self.username, self.password)
            time.sleep(1)
            
            self.log_signal.emit("📬 正在选择收件箱...")
            status, _ = mail.select('"INBOX"')
            if status != 'OK':
                raise Exception(f"选择收件箱失败: {status}")
            
            status, messages = mail.search(None, 'ALL')
            if status != 'OK':
                raise Exception("无法获取邮件列表")
            
            msg_ids = messages[0].split()
            total = len(msg_ids)
            fetch_count = min(total, self.limit)
            
            self.log_signal.emit(f"📊 收件箱共有 {total} 封邮件，准备采集最近 {fetch_count} 封...")
            
            senders = []
            # 倒序遍历，获取最新的邮件
            for i in range(total - 1, max(total - fetch_count - 1, -1), -1):
                if not self.is_running:
                    self.log_signal.emit("⏹️ 用户停止了采集任务")
                    break
                
                msg_id = msg_ids[i]
                typ, msg_data = mail.fetch(msg_id, '(BODY.PEEK[HEADER.FIELDS (FROM)])')
                
                if typ == "OK" and msg_data and msg_data[0]:
                    raw_header = msg_data[0][1]
                    msg = message_from_bytes(raw_header)
                    from_header = str(msg.get('From', ''))
                    _, addr = parseaddr(from_header)
                    if addr:
                        senders.append(addr)
                
                if len(senders) % 20 == 0:
                    self.log_signal.emit(f"📧 已扫描 {len(senders)} 个邮箱地址...")
            
            mail.close()
            mail.logout()
            
            # 去重并保持顺序
            unique_senders = self._deduplicate(senders)
            
            self.log_signal.emit(f"✅ 采集完成！原始: {len(senders)}, 去重后: {len(unique_senders)}")
            self.finish_signal.emit(unique_senders)
        
        except Exception as e:
            self.error_signal.emit(f"采集失败: {str(e)}")
    
    @staticmethod
    def _deduplicate(emails: list) -> list:
        """去重邮箱地址，保持顺序"""
        unique = []
        seen = set()
        for email in emails:
            clean = email.strip().lower()
            if clean and clean not in seen:
                seen.add(clean)
                unique.append(email)
        return unique
