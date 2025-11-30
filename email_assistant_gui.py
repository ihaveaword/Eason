#!/usr/bin/env python3
"""
Eason - 邮件助手 v1.0
Email Batch Sender Assistant
"""
import sys
import os
import time
import smtplib
import imaplib
import email
import csv
import re
from email.header import decode_header
from email.utils import parseaddr
from email.message import EmailMessage
from email import message_from_bytes
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QTabWidget, QProgressBar, QFileDialog, 
                             QMessageBox, QSpinBox, QFormLayout, QGroupBox,
                             QCheckBox, QComboBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSettings
from PyQt6.QtGui import QFont, QIcon

# --- 样式表 (macOS 风格美化 - 支持深色模式) ---
STYLESHEET = """
QMainWindow {
    background-color: palette(window);
}
QGroupBox {
    font-weight: 600;
    border: 1px solid palette(mid);
    border-radius: 8px;
    margin-top: 8px;
    padding-top: 12px;
    background-color: palette(base);
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 5px;
    color: palette(text);
}
QPushButton {
    background-color: #007AFF;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
    font-size: 13px;
    min-height: 28px;
}
QPushButton:hover {
    background-color: #0051D5;
}
QPushButton:pressed {
    background-color: #004FC4;
}
QPushButton:disabled {
    background-color: palette(mid);
    color: palette(disabled-text);
}
QPushButton#stopButton {
    background-color: #FF3B30;
}
QPushButton#stopButton:hover {
    background-color: #D70015;
}
QPushButton#secondaryButton {
    background-color: #8e8e93;
}
QPushButton#secondaryButton:hover {
    background-color: #636366;
}
QLineEdit, QTextEdit, QSpinBox, QComboBox {
    border: 1px solid palette(mid);
    border-radius: 6px;
    padding: 6px 8px;
    background-color: palette(base);
    color: palette(text);
    selection-background-color: #007AFF;
}
QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 2px solid #007AFF;
}
QProgressBar {
    border: 1px solid palette(mid);
    border-radius: 6px;
    text-align: center;
    background-color: palette(window);
    color: palette(text);
    height: 22px;
}
QProgressBar::chunk {
    background-color: #34C759;
    border-radius: 5px;
}
QLabel {
    color: palette(text);
}
QTabWidget::pane {
    border: 1px solid palette(mid);
    border-radius: 8px;
    background-color: palette(base);
    padding: 8px;
}
QTabBar::tab {
    background-color: palette(button);
    color: palette(text);
    padding: 8px 20px;
    margin-right: 4px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}
QTabBar::tab:selected {
    background-color: palette(base);
    font-weight: 600;
}
QTabBar::tab:hover:!selected {
    background-color: palette(midlight);
}
"""

# --- 工作线程：采集联系人 ---
class FetchContactsThread(QThread):
    log_signal = pyqtSignal(str)
    finish_signal = pyqtSignal(list)
    error_signal = pyqtSignal(str)

    def __init__(self, username, password, limit):
        super().__init__()
        self.username = username
        self.password = password
        self.limit = limit
        self.imap_server = 'imap.163.com'
        self.is_running = True

    def stop(self):
        self.is_running = False

    def run(self):
        try:
            self.log_signal.emit(f"🔌 正在连接 IMAP 服务器 ({self.imap_server})...")
            
            # 添加 ID 命令支持
            imaplib.Commands = {**imaplib.Commands, 'ID': ('NONAUTH',)}
            
            mail = imaplib.IMAP4_SSL(self.imap_server, 993)
            
            # 发送 ID 命令
            args = (
                b'("name" "EmailAssistant" "version" "1.0.0" '
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
            unique_senders = []
            seen = set()
            for sender in senders:
                clean_sender = sender.strip().lower()
                if clean_sender and clean_sender not in seen:
                    seen.add(clean_sender)
                    unique_senders.append(sender)
            
            self.log_signal.emit(f"✅ 采集完成！原始: {len(senders)}, 去重后: {len(unique_senders)}")
            self.finish_signal.emit(unique_senders)

        except Exception as e:
            self.error_signal.emit(f"采集失败: {str(e)}")

# --- 工作线程：发送邮件 ---
class SendEmailThread(QThread):
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int, int)
    finished_signal = pyqtSignal(int, int)  # success_count, total
    error_signal = pyqtSignal(str)

    def __init__(self, config, contact_list):
        super().__init__()
        self.cfg = config
        self.contacts = contact_list
        self.is_running = True

    def stop(self):
        self.is_running = False

    def run(self):
        smtp_server = 'smtp.163.com'
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
                    with smtplib.SMTP_SSL(smtp_server, 465, timeout=30) as server:
                        server.login(self.cfg['user'], self.cfg['pwd'])
                        self.log_signal.emit(f"🔐 批次 {batch_num} SMTP 登录成功")
                        
                        for contact in batch:
                            if not self.is_running:
                                break
                            
                            # 构建邮件
                            msg = EmailMessage()
                            msg['From'] = self.cfg['user']
                            msg['To'] = contact
                            msg['Subject'] = self.cfg['subject']
                            msg.set_content(self.cfg['body'])
                            
                            # 添加附件
                            for attachment_path in self.cfg['attachments']:
                                if attachment_path and os.path.exists(attachment_path):
                                    try:
                                        with open(attachment_path, 'rb') as f:
                                            file_data = f.read()
                                            filename = os.path.basename(attachment_path)
                                            # 根据文件扩展名判断类型
                                            ext = filename.lower().split('.')[-1]
                                            if ext in ['jpg', 'jpeg', 'png', 'gif']:
                                                maintype = 'image'
                                                subtype = ext if ext != 'jpg' else 'jpeg'
                                            elif ext == 'pdf':
                                                maintype = 'application'
                                                subtype = 'pdf'
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
                                        self.log_signal.emit(f"⚠️ 附件 {filename} 添加失败: {str(e)}")
                            
                            try:
                                server.send_message(msg)
                                success_count += 1
                                self.log_signal.emit(f"✅ [{success_count}/{total_emails}] {contact}")
                                self.progress_signal.emit(idx + (contact == batch[-1] and 1 or batch.index(contact) + 1), total_emails)
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

# --- 主窗口 ---
class EmailAssistantApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📧 Eason - 邮件助手 v1.0")
        self.setGeometry(100, 100, 850, 700)
        self.setStyleSheet(STYLESHEET)
        
        # 数据存储
        self.settings = QSettings("EmailAssistant", "BatchSender")
        self.contacts_data = []
        
        # 线程引用
        self.fetch_thread = None
        self.send_thread = None

        self.init_ui()
        self.load_config()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(16, 16, 16, 16)

        # 1. 顶部配置区
        config_group = QGroupBox("📮 账号配置 (163邮箱)")
        config_layout = QFormLayout()
        config_layout.setSpacing(8)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("your_email@163.com")
        config_layout.addRow("邮箱账号:", self.email_input)
        
        self.pwd_input = QLineEdit()
        self.pwd_input.setPlaceholderText("授权码（非登录密码）")
        self.pwd_input.setEchoMode(QLineEdit.EchoMode.Password)
        config_layout.addRow("授权码:", self.pwd_input)
        
        config_group.setLayout(config_layout)
        main_layout.addWidget(config_group)

        # 2. 中间功能区 (Tabs)
        self.tabs = QTabWidget()
        
        # --- Tab 1: 采集联系人 ---
        tab_fetch = QWidget()
        fetch_layout = QVBoxLayout(tab_fetch)
        fetch_layout.setSpacing(12)
        
        fetch_controls = QHBoxLayout()
        self.limit_spin = QSpinBox()
        self.limit_spin.setRange(10, 5000)
        self.limit_spin.setValue(200)
        self.limit_spin.setSuffix(" 封")
        
        self.btn_fetch = QPushButton("🚀 开始采集")
        self.btn_fetch.clicked.connect(self.start_fetch)
        
        self.btn_stop_fetch = QPushButton("⏹ 停止")
        self.btn_stop_fetch.setObjectName("stopButton")
        self.btn_stop_fetch.clicked.connect(self.stop_fetch)
        self.btn_stop_fetch.setEnabled(False)
        
        self.btn_save_contacts = QPushButton("💾 导出联系人")
        self.btn_save_contacts.setObjectName("secondaryButton")
        self.btn_save_contacts.clicked.connect(self.save_fetched_contacts)
        self.btn_save_contacts.setEnabled(False)

        fetch_controls.addWidget(QLabel("采集数量:"))
        fetch_controls.addWidget(self.limit_spin)
        fetch_controls.addWidget(self.btn_fetch)
        fetch_controls.addWidget(self.btn_stop_fetch)
        fetch_controls.addWidget(self.btn_save_contacts)
        fetch_controls.addStretch()
        
        self.fetch_preview = QTextEdit()
        self.fetch_preview.setPlaceholderText("📋 采集到的邮箱地址将显示在这里...\n\n点击「开始采集」按钮开始。")
        self.fetch_preview.setReadOnly(True)
        
        fetch_layout.addLayout(fetch_controls)
        fetch_layout.addWidget(self.fetch_preview)
        
        self.tabs.addTab(tab_fetch, "📥 采集联系人")

        # --- Tab 2: 批量发送 ---
        tab_send = QWidget()
        send_layout = QVBoxLayout(tab_send)
        send_layout.setSpacing(12)
        
        # 邮件内容表单
        form_layout = QFormLayout()
        form_layout.setSpacing(8)
        
        # 联系人文件
        h_contact = QHBoxLayout()
        self.contact_path_input = QLineEdit()
        self.contact_path_input.setPlaceholderText("选择联系人列表文件 (.txt 或 .csv)")
        btn_browse_contact = QPushButton("📂 浏览...")
        btn_browse_contact.setObjectName("secondaryButton")
        btn_browse_contact.clicked.connect(self.load_contacts_file)
        h_contact.addWidget(self.contact_path_input, 1)
        h_contact.addWidget(btn_browse_contact)
        form_layout.addRow("联系人列表:", h_contact)

        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("例如: 重要通知")
        form_layout.addRow("📧 邮件主题:", self.subject_input)
        
        self.body_input = QTextEdit()
        self.body_input.setPlaceholderText("请输入邮件正文内容...")
        self.body_input.setMaximumHeight(100)
        form_layout.addRow("📝 邮件正文:", self.body_input)

        # 附件区域
        h_attach = QHBoxLayout()
        self.attach_path_input = QLineEdit()
        self.attach_path_input.setReadOnly(True)
        self.attach_path_input.setPlaceholderText("可选：添加图片或PDF附件")
        btn_browse_attach = QPushButton("📎 添加附件")
        btn_browse_attach.setObjectName("secondaryButton")
        btn_browse_attach.clicked.connect(self.select_attachment)
        btn_clear_attach = QPushButton("🗑 清除")
        btn_clear_attach.setObjectName("secondaryButton")
        btn_clear_attach.clicked.connect(lambda: self.attach_path_input.clear())
        h_attach.addWidget(self.attach_path_input, 1)
        h_attach.addWidget(btn_browse_attach)
        h_attach.addWidget(btn_clear_attach)
        form_layout.addRow("📎 附件:", h_attach)

        # 批次设置
        h_batch = QHBoxLayout()
        self.batch_size_spin = QSpinBox()
        self.batch_size_spin.setRange(1, 50)
        self.batch_size_spin.setValue(10)
        self.batch_size_spin.setSuffix(" 封/批")
        self.batch_interval_spin = QSpinBox()
        self.batch_interval_spin.setRange(10, 300)
        self.batch_interval_spin.setValue(20)
        self.batch_interval_spin.setSuffix(" 秒")
        h_batch.addWidget(QLabel("批次大小:"))
        h_batch.addWidget(self.batch_size_spin)
        h_batch.addWidget(QLabel("间隔时间:"))
        h_batch.addWidget(self.batch_interval_spin)
        h_batch.addStretch()
        form_layout.addRow("⚙️ 发送策略:", h_batch)

        send_layout.addLayout(form_layout)
        
        # 发送按钮区
        h_send_btns = QHBoxLayout()
        self.btn_send = QPushButton("🚀 开始发送")
        self.btn_send.clicked.connect(self.start_send)
        self.btn_send.setMinimumHeight(36)
        
        self.btn_stop = QPushButton("⏹ 停止发送")
        self.btn_stop.setObjectName("stopButton")
        self.btn_stop.clicked.connect(self.stop_send)
        self.btn_stop.setEnabled(False)
        self.btn_stop.setMinimumHeight(36)
        
        h_send_btns.addWidget(self.btn_send)
        h_send_btns.addWidget(self.btn_stop)
        send_layout.addLayout(h_send_btns)

        self.tabs.addTab(tab_send, "📤 批量发送")
        main_layout.addWidget(self.tabs)

        # 3. 底部反馈区
        feedback_group = QGroupBox("📊 运行状态")
        feedback_layout = QVBoxLayout()
        feedback_layout.setSpacing(8)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("准备就绪")
        
        self.log_viewer = QTextEdit()
        self.log_viewer.setReadOnly(True)
        self.log_viewer.setStyleSheet("""
            background-color: #1e1e1e; 
            color: #00ff00; 
            font-family: 'SF Mono', 'Menlo', monospace;
            font-size: 12px;
            padding: 8px;
            border-radius: 6px;
        """)
        self.log_viewer.setPlaceholderText("📋 运行日志将显示在这里...")
        
        feedback_layout.addWidget(self.progress_bar)
        feedback_layout.addWidget(self.log_viewer)
        feedback_group.setLayout(feedback_layout)
        main_layout.addWidget(feedback_group, stretch=1)

    # --- 日志与配置 ---
    def log(self, message):
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        self.log_viewer.append(f"[{timestamp}] {message}")
        cursor = self.log_viewer.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.log_viewer.setTextCursor(cursor)

    def load_config(self):
        """加载上次保存的配置"""
        self.email_input.setText(self.settings.value("email", ""))
        self.pwd_input.setText(self.settings.value("pwd", ""))
        self.contact_path_input.setText(self.settings.value("last_contact_file", ""))
        self.subject_input.setText(self.settings.value("last_subject", ""))
        self.body_input.setPlainText(self.settings.value("last_body", ""))
        self.attach_path_input.setText(self.settings.value("last_attachment", ""))

    def save_config(self):
        """保存当前配置"""
        self.settings.setValue("email", self.email_input.text())
        self.settings.setValue("pwd", self.pwd_input.text())
        self.settings.setValue("last_contact_file", self.contact_path_input.text())
        self.settings.setValue("last_subject", self.subject_input.text())
        self.settings.setValue("last_body", self.body_input.toPlainText())
        self.settings.setValue("last_attachment", self.attach_path_input.text())

    # --- 采集功能 ---
    def start_fetch(self):
        user = self.email_input.text().strip()
        pwd = self.pwd_input.text().strip()
        
        if not user or not pwd:
            QMessageBox.warning(self, "⚠️ 缺少信息", "请先填写邮箱账号和授权码")
            return

        self.save_config()
        self.btn_fetch.setEnabled(False)
        self.btn_stop_fetch.setEnabled(True)
        self.btn_save_contacts.setEnabled(False)
        self.fetch_preview.clear()
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("正在采集...")
        self.log("=" * 50)
        self.log("🚀 开始采集联系人任务...")

        self.fetch_thread = FetchContactsThread(user, pwd, self.limit_spin.value())
        self.fetch_thread.log_signal.connect(self.log)
        self.fetch_thread.finish_signal.connect(self.on_fetch_finished)
        self.fetch_thread.error_signal.connect(self.on_fetch_error)
        self.fetch_thread.start()

    def stop_fetch(self):
        if self.fetch_thread and self.fetch_thread.isRunning():
            self.fetch_thread.stop()
            self.log("⏹️ 正在停止采集任务...")
            self.btn_stop_fetch.setEnabled(False)

    def on_fetch_finished(self, senders):
        self.contacts_data = senders
        self.fetch_preview.setText("\n".join(senders))
        self.btn_fetch.setEnabled(True)
        self.btn_stop_fetch.setEnabled(False)
        self.btn_save_contacts.setEnabled(True)
        self.progress_bar.setValue(100)
        self.progress_bar.setFormat(f"✅ 采集完成 - 共 {len(senders)} 个联系人")
        QMessageBox.information(self, "✅ 采集完成", f"成功采集到 {len(senders)} 个去重后的联系人！")

    def on_fetch_error(self, error_msg):
        self.log(f"❌ {error_msg}")
        self.btn_fetch.setEnabled(True)
        self.btn_stop_fetch.setEnabled(False)
        self.progress_bar.setFormat("❌ 采集失败")
        QMessageBox.critical(self, "❌ 采集失败", f"采集过程出现错误:\n\n{error_msg}")

    def save_fetched_contacts(self):
        if not self.contacts_data:
            return
        
        path, selected_filter = QFileDialog.getSaveFileName(
            self, 
            "💾 保存联系人", 
            "contacts.txt", 
            "文本文件 (*.txt);;CSV文件 (*.csv)"
        )
        
        if path:
            try:
                if path.endswith('.csv'):
                    with open(path, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(["联系人邮箱"])
                        writer.writerows([[contact] for contact in self.contacts_data])
                else:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write("\n".join(self.contacts_data))
                
                self.log(f"💾 联系人已保存到: {path}")
                QMessageBox.information(self, "✅ 保存成功", f"联系人列表已保存到:\n{path}")
            except Exception as e:
                self.log(f"❌ 保存失败: {e}")
                QMessageBox.critical(self, "❌ 保存失败", f"保存文件时出错:\n{str(e)}")

    # --- 发送功能 ---
    def load_contacts_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, 
            "📂 选择联系人文件", 
            "", 
            "文本/CSV (*.txt *.csv);;所有文件 (*.*)"
        )
        if path:
            self.contact_path_input.setText(path)

    def select_attachment(self):
        path, _ = QFileDialog.getOpenFileName(
            self, 
            "📎 选择附件", 
            "", 
            "图片/PDF (*.png *.jpg *.jpeg *.gif *.pdf);;所有文件 (*.*)"
        )
        if path:
            self.attach_path_input.setText(path)

    def parse_contacts(self, path):
        """解析联系人文件"""
        contacts = []
        try:
            if path.endswith('.csv'):
                with open(path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row and '@' in row[0]:
                            contacts.append(row[0].strip())
            else:
                with open(path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and '@' in line:
                            contacts.append(line)
        except Exception as e:
            self.log(f"❌ 读取联系人文件失败: {e}")
        
        # 去重
        return list(dict.fromkeys(contacts))

    def start_send(self):
        user = self.email_input.text().strip()
        pwd = self.pwd_input.text().strip()
        contact_path = self.contact_path_input.text().strip()
        subject = self.subject_input.text().strip()
        body = self.body_input.toPlainText().strip()

        if not all([user, pwd, contact_path, subject, body]):
            QMessageBox.warning(
                self, 
                "⚠️ 缺少信息", 
                "请确保以下信息已填写:\n\n• 邮箱账号和授权码\n• 联系人列表文件\n• 邮件主题\n• 邮件正文"
            )
            return
        
        if not os.path.exists(contact_path):
            QMessageBox.warning(self, "⚠️ 文件不存在", f"联系人文件不存在:\n{contact_path}")
            return

        self.save_config()
        
        # 解析联系人
        contacts = self.parse_contacts(contact_path)
        if not contacts:
            QMessageBox.warning(self, "⚠️ 联系人为空", "联系人文件为空或格式不正确")
            return
        
        self.log("=" * 50)
        self.log(f"📋 加载了 {len(contacts)} 个收件人")
        self.log("🚀 准备开始发送邮件...")
        
        # 配置对象
        attachments = []
        if self.attach_path_input.text().strip():
            attachments.append(self.attach_path_input.text().strip())
        
        config = {
            'user': user,
            'pwd': pwd,
            'subject': subject,
            'body': body,
            'attachments': attachments,
            'batch_size': self.batch_size_spin.value(),
            'interval': self.batch_interval_spin.value()
        }

        # UI 状态更新
        self.btn_send.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(len(contacts))
        self.progress_bar.setFormat("0/%d (0%%)" % len(contacts))

        # 启动发送线程
        self.send_thread = SendEmailThread(config, contacts)
        self.send_thread.log_signal.connect(self.log)
        self.send_thread.progress_signal.connect(self.update_progress)
        self.send_thread.finished_signal.connect(self.on_send_finished)
        self.send_thread.error_signal.connect(self.on_send_error)
        self.send_thread.start()

    def stop_send(self):
        if self.send_thread and self.send_thread.isRunning():
            self.send_thread.stop()
            self.log("⏹️ 正在停止发送任务，请稍候...")
            self.btn_stop.setEnabled(False)

    def update_progress(self, current, total):
        self.progress_bar.setValue(current)
        self.progress_bar.setFormat(f"{current}/{total} ({int(current/total*100)}%%)")

    def on_send_finished(self, success, total):
        self.btn_send.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.progress_bar.setFormat(f"✅ 完成 - 成功 {success}/{total}")
        self.log("=" * 50)
        self.log(f"🎉 发送任务结束！成功: {success}/{total}")
        
        QMessageBox.information(
            self, 
            "✅ 发送完成", 
            f"发送任务已完成！\n\n✅ 成功: {success}\n❌ 失败: {total - success}\n📊 总计: {total}"
        )

    def on_send_error(self, error_msg):
        self.log(f"❌ 严重错误: {error_msg}")
        QMessageBox.critical(self, "❌ 发送错误", f"发送过程出现严重错误:\n\n{error_msg}")

def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("邮件批量发送助手")
    app.setOrganizationName("EmailAssistant")
    app.setApplicationVersion("1.0")
    
    # 设置全局字体
    if sys.platform == 'darwin':  # macOS
        font = QFont("SF Pro Text", 13)
    else:
        font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = EmailAssistantApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
