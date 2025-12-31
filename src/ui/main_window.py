"""
主窗口界面
包含采集联系人和批量发送两个功能标签页
"""
import os
import time
import csv
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QTextEdit, 
    QTabWidget, QProgressBar, QFileDialog, QMessageBox, 
    QSpinBox, QFormLayout, QGroupBox, QCheckBox, QComboBox
)
from PyQt6.QtCore import QSettings
from ..core import EmailSender, ContactFetcher, ConfigManager
from ..utils import read_contacts, export_contacts
from .styles import STYLESHEET

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📧 Eason - 邮件助手 v2.0")
        self.setGeometry(100, 100, 850, 700)
        self.setStyleSheet(STYLESHEET)
        
        # 数据存储
        self.config_manager = ConfigManager()
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
        
        # HTML模板选项（新增）
        h_template = QHBoxLayout()
        self.use_template_checkbox = QCheckBox("使用HTML模板")
        self.use_template_checkbox.stateChanged.connect(self.toggle_template_mode)
        
        self.template_combo = QComboBox()
        self.template_combo.setEnabled(False)
        self.template_combo.addItem("选择模板...", "")
        # 加载模板列表
        try:
            from ..templates import TemplateEngine
            engine = TemplateEngine()
            templates = engine.list_templates()
            for tpl in templates:
                self.template_combo.addItem(
                    f"{tpl['display_name']} - {tpl['description']}", 
                    tpl['name']
                )
        except Exception:
            pass
        
        self.btn_config_vars = QPushButton("⚙️ 配置变量")
        self.btn_config_vars.setObjectName("secondaryButton")
        self.btn_config_vars.setEnabled(False)
        self.btn_config_vars.clicked.connect(self.config_template_variables)
        
        self.btn_preview = QPushButton("🔍 预览")
        self.btn_preview.setObjectName("secondaryButton")
        self.btn_preview.setEnabled(False)
        self.btn_preview.clicked.connect(self.preview_template)
        
        h_template.addWidget(self.use_template_checkbox)
        h_template.addWidget(self.template_combo, 1)
        h_template.addWidget(self.btn_config_vars)
        h_template.addWidget(self.btn_preview)
        form_layout.addRow("🎨 邮件模板:", h_template)
        
        # 初始化模板变量
        self.template_vars = {}
        
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
        self.email_input.setText(self.config_manager.settings.value("email", ""))
        self.pwd_input.setText(self.config_manager.settings.value("pwd", ""))
        self.contact_path_input.setText(self.config_manager.settings.value("last_contact_file", ""))
        self.subject_input.setText(self.config_manager.settings.value("last_subject", ""))
        self.body_input.setPlainText(self.config_manager.settings.value("last_body", ""))
        self.attach_path_input.setText(self.config_manager.settings.value("last_attachment", ""))

    def save_config(self):
        """保存当前配置"""
        self.config_manager.settings.setValue("email", self.email_input.text())
        self.config_manager.settings.setValue("pwd", self.pwd_input.text())
        self.config_manager.settings.setValue("last_contact_file", self.contact_path_input.text())
        self.config_manager.settings.setValue("last_subject", self.subject_input.text())
        self.config_manager.settings.setValue("last_body", self.body_input.toPlainText())
        self.config_manager.settings.setValue("last_attachment", self.attach_path_input.text())

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

        self.fetch_thread = ContactFetcher(user, pwd, self.limit_spin.value())
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
            'interval': self.batch_interval_spin.value(),
            # HTML模板配置
            'use_template': self.use_template_checkbox.isChecked(),
            'template_name': self.template_combo.currentData() or '',
            **self.template_vars  # 合并模板变量
        }

        # UI 状态更新
        self.btn_send.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(len(contacts))
        self.progress_bar.setFormat("0/%d (0%%)" % len(contacts))

        # 启动发送线程
        self.send_thread = EmailSender(config, contacts)
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
    
    def toggle_template_mode(self, state):
        """切换模板模式"""
        from PyQt6.QtCore import Qt
        use_template = (state == Qt.CheckState.Checked.value)
        
        # 启用/禁用相关控件
        self.template_combo.setEnabled(use_template)
        self.btn_config_vars.setEnabled(use_template)
        self.btn_preview.setEnabled(use_template)
        
        # 更新提示信息
        if use_template:
            self.body_input.setPlaceholderText("使用HTML模板时，此处内容作为纯文本备用...")
        else:
            self.body_input.setPlaceholderText("请输入邮件正文内容...")
    
    def config_template_variables(self):
        """配置模板变量"""
        from .variable_config_dialog import VariableConfigDialog
        
        # 获取当前模板的必填变量
        template_name = self.template_combo.currentData()
        required_vars = []
        if template_name:
            try:
                from ..templates import TemplateEngine
                engine = TemplateEngine()
                templates = engine.list_templates()
                for tpl in templates:
                    if tpl['name'] == template_name:
                        required_vars = tpl.get('required_vars', [])
                        break
            except Exception:
                pass
        
        dialog = VariableConfigDialog(self.template_vars, required_vars, self)
        if dialog.exec():
            self.template_vars = dialog.get_variables()
            QMessageBox.information(self, "✅ 配置成功", "模板变量配置已保存")
    
    def preview_template(self):
        """预览模板"""
        from .template_preview import TemplatePreviewDialog
        
        template_name = self.template_combo.currentData()
        if not template_name:
            QMessageBox.warning(self, "⚠️ 未选择模板", "请先选择一个模板")
            return
        
        try:
            from ..templates import TemplateEngine
            from datetime import datetime
            
            engine = TemplateEngine()
            
            # 准备预览变量
            preview_vars = {
                'recipient_email': 'example@test.com',
                'recipient_name': '张三',
                'sender_name': self.template_vars.get('sender_name', '测试发件人'),
                'sender_company': self.template_vars.get('sender_company', '测试公司'),
                'sender_email': self.email_input.text() or 'test@example.com',
                'date': datetime.now().strftime('%Y年%m月%d日'),
                'time': datetime.now().strftime('%H:%M'),
                'year': str(datetime.now().year),
                'custom_1': self.template_vars.get('custom_1', '自定义内容1'),
                'custom_2': self.template_vars.get('custom_2', '自定义内容2'),
                'custom_3': self.template_vars.get('custom_3', '自定义内容3'),
            }
            
            html_content = engine.render(template_name, preview_vars)
            
            dialog = TemplatePreviewDialog(html_content, self)
            dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "❌ 预览失败", f"模板预览失败:\n\n{str(e)}")

def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("邮件批量发送助手")
    app.setOrganizationName("EmailAssistant")
    app.setApplicationVersion("1.0")
