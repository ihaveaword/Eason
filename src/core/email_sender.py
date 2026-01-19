"""
邮件发送模块
支持批量发送、附件、进度追踪、HTML模板
支持多种邮箱：163、126、QQ、Gmail、Outlook 等
"""
import os
import time
import smtplib
from datetime import datetime
from email.message import EmailMessage
from typing import List, Dict, Optional
from PyQt6.QtCore import QThread, pyqtSignal
from .email_config import get_smtp_server, get_smtp_port, use_starttls


class EmailSender(QThread):
    """邮件发送线程"""
    
    # 信号定义（与 main_window_v2.py 匹配）
    progress = pyqtSignal(int, int, str)  # current, total, email
    result = pyqtSignal(int, int)  # success_count, failed_count
    error = pyqtSignal(str)
    finished = pyqtSignal()
    finished = pyqtSignal()
    batch_done = pyqtSignal(int, int)  # batch_num, wait_time
    wait_progress = pyqtSignal(int)    # remaining_seconds
    
    def __init__(self, user: str, pwd: str, contacts: List[str], 
                 subject: str, body: str, attachment: Optional[str] = None,
                 batch_size: int = 10, interval: int = 5,
                 html_body: Optional[str] = None):
        super().__init__()
        
        self.user = user
        self.pwd = pwd
        self.contacts = contacts
        self.subject = subject
        self.body = body
        self.attachment = attachment
        self.batch_size = batch_size
        self.interval = interval
        self.html_body = html_body
        
        # 自动检测邮箱服务器
        self.smtp_server = get_smtp_server(user)
        self.smtp_port = get_smtp_port(user)
        self.use_tls = use_starttls(user)
        
        self.is_running = True
    
    def stop(self):
        """停止发送"""
        self.is_running = False
    
    def _connect_smtp(self):
        """建立 SMTP 连接（支持 SSL 和 STARTTLS）"""
        if self.use_tls:
            # Outlook 等使用 STARTTLS
            server = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=30)
            server.starttls()
        else:
            # 163、QQ 等使用 SSL
            server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, timeout=30)
        return server
    
    def run(self):
        """执行发送任务"""
        total_emails = len(self.contacts)
        success_count = 0
        failed_count = 0
        
        try:
            for idx in range(0, total_emails, self.batch_size):
                if not self.is_running:
                    break
                
                batch = self.contacts[idx:idx + self.batch_size]
                batch_num = idx // self.batch_size + 1
                
                try:
                    with self._connect_smtp() as server:
                        server.login(self.user, self.pwd)
                        
                        for i, contact in enumerate(batch):
                            if not self.is_running:
                                break
                            
                            # 处理联系人格式（可能是 email 或 dict）
                            if isinstance(contact, dict):
                                email = contact.get('email', '')
                            else:
                                email = str(contact)
                            
                            if not email:
                                continue
                            
                            # 构建并发送邮件
                            msg = self._build_email(email)
                            
                            try:
                                server.send_message(msg)
                                success_count += 1
                                self.progress.emit(idx + i + 1, total_emails, email)
                            except Exception as e:
                                failed_count += 1
                                self.error.emit(f"发送失败 {email}: {str(e)}")
                
                except smtplib.SMTPAuthenticationError as e:
                    self.error.emit(f"SMTP认证失败: 请检查邮箱账号和授权码是否正确")
                    break
                except smtplib.SMTPServerDisconnected:
                    self.error.emit(f"批次 {batch_num} 连接断开，将在下一批次重连")
                except Exception as e:
                    self.error.emit(f"批次 {batch_num} 发生错误: {str(e)}")
                
                # 批次间隔
                if idx + self.batch_size < total_emails and self.is_running:
                    self.batch_done.emit(batch_num, self.interval)
                    for i in range(self.interval):
                        if not self.is_running:
                            break
                        remaining = self.interval - i
                        self.wait_progress.emit(remaining)
                        time.sleep(1)
            
            self.result.emit(success_count, failed_count)
        
        except Exception as e:
            self.error.emit(f"发送过程发生严重错误: {str(e)}")
            self.result.emit(success_count, failed_count)
        
        finally:
            self.finished.emit()
    
    def _build_email(self, recipient: str) -> EmailMessage:
        """构建邮件（支持HTML模板）"""
        msg = EmailMessage()
        msg['From'] = self.user
        msg['To'] = recipient
        msg['Subject'] = self.subject
        
        # 判断是否使用HTML模板
        if self.html_body:
            # 设置多部分内容（纯文本备用 + HTML）
            msg.set_content(self.body or '请使用支持HTML的邮件客户端查看此邮件')
            msg.add_alternative(self.html_body, subtype='html')
        else:
            # 纯文本模式
            msg.set_content(self.body)
        
        # 添加附件
        if self.attachment and os.path.exists(self.attachment):
            self._add_attachment(msg, self.attachment)
        
        return msg
    
    def _add_attachment(self, msg: EmailMessage, filepath: str):
        """添加附件到邮件"""
        try:
            with open(filepath, 'rb') as f:
                file_data = f.read()
                filename = os.path.basename(filepath)
                
                # 根据文件扩展名判断类型
                ext = filename.lower().split('.')[-1]
                if ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                    maintype = 'image'
                    subtype = ext if ext != 'jpg' else 'jpeg'
                elif ext == 'pdf':
                    maintype = 'application'
                    subtype = 'pdf'
                elif ext in ['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx']:
                    maintype = 'application'
                    subtype = 'octet-stream'
                else:
                    maintype = 'application'
                    subtype = 'octet-stream'
                
                msg.add_attachment(
                    file_data,
                    maintype=maintype,
                    subtype=subtype,
                    filename=filename
                )
        except Exception as e:
            self.error.emit(f"⚠️ 附件 {os.path.basename(filepath)} 添加失败: {str(e)}")
