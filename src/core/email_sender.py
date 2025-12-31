"""
邮件发送模块
支持批量发送、附件、进度追踪
"""
import os
import time
import smtplib
from email.message import EmailMessage
from typing import List, Dict
from PyQt6.QtCore import QThread, pyqtSignal


class EmailSender(QThread):
    """邮件发送线程"""
    
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int, int)
    finished_signal = pyqtSignal(int, int)  # success_count, total
    error_signal = pyqtSignal(str)
    
    def __init__(self, config: Dict, contact_list: List[str], smtp_server: str = 'smtp.163.com'):
        super().__init__()
        self.cfg = config
        self.contacts = contact_list
        self.smtp_server = smtp_server
        self.is_running = True
    
    def stop(self):
        """停止发送"""
        self.is_running = False
    
    def run(self):
        """执行发送任务"""
        total_emails = len(self.contacts)
        batch_size = self.cfg['batch_size']
        interval = self.cfg['interval']
        
        success_count = 0
        failed_count = 0
        
        try:
            for idx in range(0, total_emails, batch_size):
                if not self.is_running:
                    self.log_signal.emit("⏹️ 用户停止了发送任务")
                    break
                
                batch = self.contacts[idx:idx+batch_size]
                batch_num = idx // batch_size + 1
                self.log_signal.emit(f"📦 批次 {batch_num}: 准备发送 {len(batch)} 封邮件...")
                
                try:
                    with smtplib.SMTP_SSL(self.smtp_server, 465, timeout=30) as server:
                        server.login(self.cfg['user'], self.cfg['pwd'])
                        self.log_signal.emit(f"🔐 批次 {batch_num} SMTP 登录成功")
                        
                        for i, contact in enumerate(batch):
                            if not self.is_running:
                                break
                            
                            # 构建邮件
                            msg = self._build_email(contact)
                            
                            try:
                                server.send_message(msg)
                                success_count += 1
                                self.log_signal.emit(f"✅ [{success_count}/{total_emails}] {contact}")
                                self.progress_signal.emit(idx + i + 1, total_emails)
                            except Exception as e:
                                failed_count += 1
                                self.log_signal.emit(f"❌ 发送失败 {contact}: {str(e)}")
                
                except smtplib.SMTPServerDisconnected:
                    self.log_signal.emit(f"⚠️ 批次 {batch_num} 连接断开，将在下一批次重连")
                except Exception as e:
                    self.log_signal.emit(f"❌ 批次 {batch_num} 发生错误: {str(e)}")
                
                # 批次间隔
                if idx + batch_size < total_emails and self.is_running:
                    self.log_signal.emit(f"⏸️ 批次完成，等待 {interval} 秒后继续...")
                    for _ in range(interval):
                        if not self.is_running:
                            break
                        time.sleep(1)
            
            self.log_signal.emit(f"🎉 发送任务完成！成功: {success_count}, 失败: {failed_count}, 总计: {total_emails}")
            self.finished_signal.emit(success_count, total_emails)
        
        except Exception as e:
            self.error_signal.emit(f"发送过程发生严重错误: {str(e)}")
            self.finished_signal.emit(success_count, total_emails)
    
    def _build_email(self, recipient: str) -> EmailMessage:
        """构建邮件"""
        msg = EmailMessage()
        msg['From'] = self.cfg['user']
        msg['To'] = recipient
        msg['Subject'] = self.cfg['subject']
        msg.set_content(self.cfg['body'])
        
        # 添加附件
        for attachment_path in self.cfg.get('attachments', []):
            if attachment_path and os.path.exists(attachment_path):
                self._add_attachment(msg, attachment_path)
        
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
            self.log_signal.emit(f"⚠️ 附件 {os.path.basename(filepath)} 添加失败: {str(e)}")
