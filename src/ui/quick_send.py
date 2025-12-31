"""
快捷发送弹窗 & 联系人选择弹窗
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QComboBox, QFrame, QCheckBox,
    QScrollArea, QWidget, QMessageBox, QFileDialog, QProgressBar
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont
from ..core import ContactDatabase, EmailSender, get_email_config


class QuickSendDialog(QDialog):
    """快捷发送邮件弹窗"""
    
    def __init__(self, contact: dict, sender_email: str = '', sender_pwd: str = '', parent=None):
        super().__init__(parent)
        self.contact = contact
        self.sender_email = sender_email
        self.sender_pwd = sender_pwd
        self.send_thread = None
        
        self.setWindowTitle("快捷发送")
        self.setMinimumSize(500, 450)
        self.setModal(True)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # 收件人信息
        recipient_frame = QFrame()
        recipient_frame.setStyleSheet("""
            QFrame {
                background: rgba(79, 70, 229, 0.1);
                border: 1px solid rgba(79, 70, 229, 0.3);
                border-radius: 8px;
                padding: 12px;
            }
        """)
        recipient_layout = QHBoxLayout(recipient_frame)
        
        recipient_icon = QLabel("📧")
        recipient_icon.setStyleSheet("font-size: 24px;")
        recipient_layout.addWidget(recipient_icon)
        
        recipient_info = QVBoxLayout()
        name = self.contact.get('name') or '未命名'
        email = self.contact.get('email', '')
        
        name_label = QLabel(name)
        name_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #E5E7EB;")
        email_label = QLabel(email)
        email_label.setStyleSheet("font-size: 13px; color: #9CA3AF;")
        
        recipient_info.addWidget(name_label)
        recipient_info.addWidget(email_label)
        recipient_layout.addLayout(recipient_info)
        recipient_layout.addStretch()
        
        layout.addWidget(recipient_frame)
        
        # 主题
        subject_label = QLabel("主题")
        subject_label.setStyleSheet("color: #9CA3AF; font-size: 12px; font-weight: 600;")
        layout.addWidget(subject_label)
        
        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("邮件主题...")
        self.subject_input.setStyleSheet("""
            QLineEdit {
                background: #1A1A2E;
                border: 1px solid #2D2D3D;
                border-radius: 6px;
                padding: 10px 12px;
                color: #E5E7EB;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #4F46E5;
            }
        """)
        layout.addWidget(self.subject_input)
        
        # 正文
        body_label = QLabel("正文")
        body_label.setStyleSheet("color: #9CA3AF; font-size: 12px; font-weight: 600;")
        layout.addWidget(body_label)
        
        self.body_input = QTextEdit()
        self.body_input.setPlaceholderText("邮件内容...\n\n提示：使用 {name} 插入收件人姓名")
        self.body_input.setStyleSheet("""
            QTextEdit {
                background: #1A1A2E;
                border: 1px solid #2D2D3D;
                border-radius: 6px;
                padding: 10px 12px;
                color: #E5E7EB;
                font-size: 14px;
            }
            QTextEdit:focus {
                border-color: #4F46E5;
            }
        """)
        layout.addWidget(self.body_input, 1)
        
        # 附件
        attach_row = QHBoxLayout()
        self.attach_btn = QPushButton("📎 添加附件")
        self.attach_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 1px dashed #3D3D5C;
                border-radius: 6px;
                padding: 8px 16px;
                color: #9CA3AF;
            }
            QPushButton:hover {
                border-color: #4F46E5;
                color: #A5B4FC;
            }
        """)
        self.attach_btn.clicked.connect(self.add_attachment)
        attach_row.addWidget(self.attach_btn)
        
        self.attach_label = QLabel("")
        self.attach_label.setStyleSheet("color: #6B7280; font-size: 12px;")
        attach_row.addWidget(self.attach_label)
        attach_row.addStretch()
        
        layout.addLayout(attach_row)
        
        self.attachment_path = ""
        
        # 进度条（默认隐藏）
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background: #1A1A2E;
                border: none;
                border-radius: 4px;
                height: 6px;
            }
            QProgressBar::chunk {
                background: #4F46E5;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # 按钮
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        
        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 1px solid #3D3D5C;
                border-radius: 6px;
                padding: 10px 24px;
                color: #9CA3AF;
            }
            QPushButton:hover {
                border-color: #6B7280;
                color: #E5E7EB;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        
        self.send_btn = QPushButton("📤 发送")
        self.send_btn.setStyleSheet("""
            QPushButton {
                background: #4F46E5;
                border: none;
                border-radius: 6px;
                padding: 10px 24px;
                color: white;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #4338CA;
            }
            QPushButton:disabled {
                background: #3D3D5C;
                color: #6B7280;
            }
        """)
        self.send_btn.clicked.connect(self.send_email)
        btn_row.addWidget(self.send_btn)
        
        layout.addLayout(btn_row)
    
    def add_attachment(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择附件")
        if path:
            self.attachment_path = path
            filename = path.split('/')[-1]
            self.attach_label.setText(f"📎 {filename}")
    
    def send_email(self):
        if not self.sender_email or not self.sender_pwd:
            QMessageBox.warning(self, "配置缺失", "请先在「账号设置」中配置发件邮箱")
            return
        
        subject = self.subject_input.text().strip()
        body = self.body_input.toPlainText().strip()
        
        if not subject:
            QMessageBox.warning(self, "缺少信息", "请填写邮件主题")
            return
        
        if not body:
            QMessageBox.warning(self, "缺少信息", "请填写邮件正文")
            return
        
        # 替换变量
        name = self.contact.get('name') or self.contact.get('email', '').split('@')[0]
        body = body.replace('{name}', name)
        
        self.send_btn.setEnabled(False)
        self.send_btn.setText("发送中...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 不确定进度
        
        # 获取SMTP配置
        config = get_email_config(self.sender_email)
        
        try:
            sender = EmailSender(
                self.sender_email, 
                self.sender_pwd,
                smtp_server=config['smtp_server'],
                smtp_port=config['smtp_port']
            )
            
            success = sender.send_email(
                to_email=self.contact['email'],
                subject=subject,
                body=body,
                attachment=self.attachment_path if self.attachment_path else None
            )
            
            self.progress_bar.setVisible(False)
            
            if success:
                # 记录发送
                db = ContactDatabase()
                db.record_send(self.contact['email'])
                
                QMessageBox.information(self, "✅ 发送成功", f"邮件已发送给 {self.contact['email']}")
                self.accept()
            else:
                self.send_btn.setEnabled(True)
                self.send_btn.setText("📤 发送")
                QMessageBox.critical(self, "❌ 发送失败", "邮件发送失败，请检查网络和配置")
        
        except Exception as e:
            self.progress_bar.setVisible(False)
            self.send_btn.setEnabled(True)
            self.send_btn.setText("📤 发送")
            QMessageBox.critical(self, "❌ 发送失败", f"发送失败: {str(e)}")


class ContactSelectDialog(QDialog):
    """联系人/分组选择弹窗"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = ContactDatabase()
        self.selected_contacts = []
        self.selected_groups = set()
        
        self.setWindowTitle("选择联系人")
        self.setMinimumSize(500, 550)
        self.setModal(True)
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 搜索联系人...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: #1A1A2E;
                border: 1px solid #2D2D3D;
                border-radius: 6px;
                padding: 10px 12px;
                color: #E5E7EB;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #4F46E5;
            }
        """)
        self.search_input.textChanged.connect(self.filter_contacts)
        layout.addWidget(self.search_input)
        
        # 分组快选区
        group_label = QLabel("📂 分组快选")
        group_label.setStyleSheet("color: #9CA3AF; font-size: 12px; font-weight: 600;")
        layout.addWidget(group_label)
        
        self.group_frame = QFrame()
        self.group_frame.setStyleSheet("""
            QFrame {
                background: #1A1A2E;
                border: 1px solid #2D2D3D;
                border-radius: 8px;
            }
        """)
        self.group_layout = QVBoxLayout(self.group_frame)
        self.group_layout.setContentsMargins(12, 12, 12, 12)
        self.group_layout.setSpacing(8)
        
        layout.addWidget(self.group_frame)
        
        # 联系人列表区
        contact_label = QLabel("👥 联系人列表")
        contact_label.setStyleSheet("color: #9CA3AF; font-size: 12px; font-weight: 600;")
        layout.addWidget(contact_label)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                background: #1A1A2E;
                border: 1px solid #2D2D3D;
                border-radius: 8px;
            }
        """)
        
        self.contact_container = QWidget()
        self.contact_layout = QVBoxLayout(self.contact_container)
        self.contact_layout.setContentsMargins(12, 12, 12, 12)
        self.contact_layout.setSpacing(4)
        self.contact_layout.addStretch()
        
        scroll.setWidget(self.contact_container)
        layout.addWidget(scroll, 1)
        
        # 底部统计和按钮
        bottom_row = QHBoxLayout()
        
        self.count_label = QLabel("已选: 0 人")
        self.count_label.setStyleSheet("color: #A5B4FC; font-weight: 600;")
        bottom_row.addWidget(self.count_label)
        
        bottom_row.addStretch()
        
        clear_btn = QPushButton("清空")
        clear_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #9CA3AF;
                padding: 8px 16px;
            }
            QPushButton:hover {
                color: #EF4444;
            }
        """)
        clear_btn.clicked.connect(self.clear_selection)
        bottom_row.addWidget(clear_btn)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 1px solid #3D3D5C;
                border-radius: 6px;
                padding: 10px 24px;
                color: #9CA3AF;
            }
            QPushButton:hover {
                border-color: #6B7280;
                color: #E5E7EB;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        bottom_row.addWidget(cancel_btn)
        
        confirm_btn = QPushButton("✓ 确定")
        confirm_btn.setStyleSheet("""
            QPushButton {
                background: #4F46E5;
                border: none;
                border-radius: 6px;
                padding: 10px 24px;
                color: white;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #4338CA;
            }
        """)
        confirm_btn.clicked.connect(self.confirm_selection)
        bottom_row.addWidget(confirm_btn)
        
        layout.addLayout(bottom_row)
        
        self.group_checkboxes = {}
        self.contact_checkboxes = {}
    
    def load_data(self):
        # 加载分组
        groups = self.db.get_groups()
        
        for g in groups:
            cb = QCheckBox(f"{g['icon']}  {g['name']} ({g['contact_count']}人)")
            cb.setProperty('group_id', g['id'])
            cb.setProperty('count', g['contact_count'])
            cb.setStyleSheet("""
                QCheckBox {
                    color: #E5E7EB;
                    font-size: 13px;
                    padding: 6px;
                }
                QCheckBox:hover {
                    background: rgba(255, 255, 255, 0.05);
                    border-radius: 4px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
            """)
            cb.stateChanged.connect(self.on_group_changed)
            self.group_layout.addWidget(cb)
            self.group_checkboxes[g['id']] = cb
        
        # 加载联系人
        self.all_contacts = self.db.get_contacts()
        self.display_contacts(self.all_contacts)
    
    def display_contacts(self, contacts):
        # 清空旧的
        while self.contact_layout.count() > 1:
            item = self.contact_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.contact_checkboxes.clear()
        
        for c in contacts:
            cb = QCheckBox(f"{c['email']}  -  {c['name'] or '未命名'}")
            cb.setProperty('contact_id', c['id'])
            cb.setProperty('email', c['email'])
            cb.setProperty('name', c['name'])
            cb.setProperty('group_id', c['group_id'])
            cb.setStyleSheet("""
                QCheckBox {
                    color: #D1D5DB;
                    font-size: 12px;
                    padding: 4px;
                }
                QCheckBox:hover {
                    background: rgba(255, 255, 255, 0.03);
                    border-radius: 4px;
                }
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                }
            """)
            cb.stateChanged.connect(self.on_contact_changed)
            
            # 插入到 stretch 之前
            self.contact_layout.insertWidget(self.contact_layout.count() - 1, cb)
            self.contact_checkboxes[c['id']] = cb
    
    def on_group_changed(self):
        """分组选择变化"""
        sender = self.sender()
        group_id = sender.property('group_id')
        is_checked = sender.isChecked()
        
        if is_checked:
            self.selected_groups.add(group_id)
        else:
            self.selected_groups.discard(group_id)
        
        # 联动更新该分组下的联系人
        for cid, cb in self.contact_checkboxes.items():
            if cb.property('group_id') == group_id:
                cb.blockSignals(True)
                cb.setChecked(is_checked)
                cb.blockSignals(False)
        
        self.update_count()
    
    def on_contact_changed(self):
        """联系人选择变化"""
        self.update_count()
    
    def filter_contacts(self):
        """搜索过滤"""
        search = self.search_input.text().strip().lower()
        
        for cid, cb in self.contact_checkboxes.items():
            email = cb.property('email') or ''
            name = cb.property('name') or ''
            visible = search in email.lower() or search in name.lower()
            cb.setVisible(visible)
    
    def clear_selection(self):
        """清空选择"""
        for cb in self.group_checkboxes.values():
            cb.blockSignals(True)
            cb.setChecked(False)
            cb.blockSignals(False)
        
        for cb in self.contact_checkboxes.values():
            cb.blockSignals(True)
            cb.setChecked(False)
            cb.blockSignals(False)
        
        self.selected_groups.clear()
        self.update_count()
    
    def update_count(self):
        """更新选中计数"""
        count = sum(1 for cb in self.contact_checkboxes.values() if cb.isChecked())
        self.count_label.setText(f"已选: {count} 人")
    
    def confirm_selection(self):
        """确认选择"""
        self.selected_contacts = []
        
        for cid, cb in self.contact_checkboxes.items():
            if cb.isChecked():
                self.selected_contacts.append({
                    'email': cb.property('email'),
                    'name': cb.property('name') or ''
                })
        
        if not self.selected_contacts:
            QMessageBox.warning(self, "提示", "请至少选择一个联系人")
            return
        
        self.accept()
    
    def get_selected_contacts(self) -> list:
        """获取选中的联系人"""
        return self.selected_contacts
