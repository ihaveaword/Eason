"""
联系人管理页面
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QFrame, QScrollArea, QMenu, QMessageBox, QDialog,
    QFormLayout, QComboBox, QTextEdit, QCheckBox, QAbstractItemView,
    QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QBrush, QAction
from ..core import ContactDatabase


class GroupButton(QPushButton):
    """分组按钮"""
    def __init__(self, name: str, count: int, icon: str = "📁", 
                 color: str = "#4F46E5", group_id: int = None, parent=None):
        super().__init__(parent)
        self.group_id = group_id
        self.group_name = name
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_text(name, count, icon)
        
        self.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: 8px;
                padding: 10px 12px;
                text-align: left;
                font-size: 13px;
                color: #E5E7EB;
            }}
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.08);
            }}
            QPushButton:checked {{
                background: rgba(79, 70, 229, 0.3);
                color: #A5B4FC;
            }}
        """)
    
    def update_text(self, name: str, count: int, icon: str = "📁"):
        self.setText(f"{icon}  {name}  ({count})")
        self.group_name = name


class ContactEditDialog(QDialog):
    """联系人编辑对话框"""
    def __init__(self, contact: dict = None, groups: list = None, parent=None):
        super().__init__(parent)
        self.contact = contact or {}
        self.groups = groups or []
        self.setWindowTitle("编辑联系人" if contact else "添加联系人")
        self.setMinimumWidth(400)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        form = QFormLayout()
        form.setSpacing(12)
        
        # 邮箱
        self.email_input = QLineEdit()
        self.email_input.setText(self.contact.get('email', ''))
        self.email_input.setPlaceholderText("example@email.com")
        if self.contact.get('id'):  # 编辑模式，邮箱不可改
            self.email_input.setEnabled(False)
        form.addRow("邮箱:", self.email_input)
        
        # 姓名
        self.name_input = QLineEdit()
        self.name_input.setText(self.contact.get('name', ''))
        self.name_input.setPlaceholderText("联系人姓名")
        form.addRow("姓名:", self.name_input)
        
        # 分组
        self.group_combo = QComboBox()
        self.group_combo.addItem("未分组", None)
        for g in self.groups:
            self.group_combo.addItem(f"{g['icon']}  {g['name']}", g['id'])
        
        # 设置当前分组
        current_group_id = self.contact.get('group_id')
        for i in range(self.group_combo.count()):
            if self.group_combo.itemData(i) == current_group_id:
                self.group_combo.setCurrentIndex(i)
                break
        form.addRow("分组:", self.group_combo)
        
        # 备注
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("备注信息...")
        self.notes_input.setText(self.contact.get('notes', ''))
        self.notes_input.setMaximumHeight(80)
        form.addRow("备注:", self.notes_input)
        
        layout.addLayout(form)
        
        # 按钮
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        
        save_btn = QPushButton("保存")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.accept)
        btn_row.addWidget(save_btn)
        
        layout.addLayout(btn_row)
    
    def get_data(self) -> dict:
        return {
            'email': self.email_input.text().strip(),
            'name': self.name_input.text().strip(),
            'group_id': self.group_combo.currentData(),
            'notes': self.notes_input.toPlainText().strip(),
        }


class GroupEditDialog(QDialog):
    """分组编辑对话框"""
    def __init__(self, group: dict = None, parent=None):
        super().__init__(parent)
        self.group = group or {}
        self.setWindowTitle("编辑分组" if group else "新建分组")
        self.setMinimumWidth(350)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        form = QFormLayout()
        form.setSpacing(12)
        
        # 名称
        self.name_input = QLineEdit()
        self.name_input.setText(self.group.get('name', ''))
        self.name_input.setPlaceholderText("分组名称")
        form.addRow("名称:", self.name_input)
        
        # 图标
        self.icon_combo = QComboBox()
        icons = ['📁', '👥', '🏢', '👔', '⭐', '💼', '🎯', '📌', '💡', '🔥']
        for icon in icons:
            self.icon_combo.addItem(icon)
        current_icon = self.group.get('icon', '📁')
        if current_icon in icons:
            self.icon_combo.setCurrentIndex(icons.index(current_icon))
        form.addRow("图标:", self.icon_combo)
        
        layout.addLayout(form)
        
        # 按钮
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        
        save_btn = QPushButton("保存")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.accept)
        btn_row.addWidget(save_btn)
        
        layout.addLayout(btn_row)
    
    def get_data(self) -> dict:
        return {
            'name': self.name_input.text().strip(),
            'icon': self.icon_combo.currentText(),
        }


class ContactManagerWidget(QWidget):
    """联系人管理组件"""
    
    # 信号：选中联系人用于发送
    contacts_selected_for_send = pyqtSignal(list)
    # 信号：快捷发送单个联系人
    quick_send_requested = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = ContactDatabase()
        self.current_group_id = None  # None = 全部
        self.selected_contacts = []
        self.is_dark_theme = True  # 默认深色主题
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # ===== 左侧分组列表 =====
        self.group_panel = QFrame()
        self.group_panel.setObjectName("groupPanel")
        self.group_panel.setFixedWidth(200)
        
        group_layout = QVBoxLayout(self.group_panel)
        group_layout.setContentsMargins(12, 16, 12, 16)
        group_layout.setSpacing(8)
        
        # 分组标题
        group_header = QHBoxLayout()
        self.group_title = QLabel("📂 分组")
        group_header.addWidget(self.group_title)
        group_header.addStretch()
        
        self.add_group_btn = QPushButton("+")
        self.add_group_btn.setFixedSize(24, 24)
        self.add_group_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_group_btn.clicked.connect(self.add_group)
        group_header.addWidget(self.add_group_btn)
        group_layout.addLayout(group_header)
        
        # 全部联系人按钮
        self.all_btn = GroupButton("全部联系人", 0, "📋", group_id=None)
        self.all_btn.setChecked(True)
        self.all_btn.clicked.connect(lambda: self.select_group(None))
        group_layout.addWidget(self.all_btn)
        
        # 分组按钮容器
        self.group_buttons_layout = QVBoxLayout()
        self.group_buttons_layout.setSpacing(4)
        group_layout.addLayout(self.group_buttons_layout)
        
        group_layout.addStretch()
        
        layout.addWidget(self.group_panel)
        
        # ===== 右侧联系人列表 =====
        content_panel = QFrame()
        content_panel.setObjectName("contentPanel")
        content_layout = QVBoxLayout(content_panel)
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(16)
        
        # 顶部工具栏
        toolbar = QHBoxLayout()
        toolbar.setSpacing(12)
        
        # 全选复选框
        self.select_all_checkbox = QCheckBox("全选")
        self.select_all_checkbox.stateChanged.connect(self.toggle_select_all)
        toolbar.addWidget(self.select_all_checkbox)
        
        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 搜索联系人...")
        self.search_input.setMaximumWidth(300)
        self.search_input.textChanged.connect(self.on_search)
        toolbar.addWidget(self.search_input)
        
        toolbar.addStretch()
        
        # 操作按钮
        add_btn = QPushButton("+ 添加联系人")
        add_btn.setObjectName("primaryButton")
        add_btn.clicked.connect(self.add_contact)
        toolbar.addWidget(add_btn)
        
        import_btn = QPushButton("📥 导入")
        import_btn.setObjectName("secondaryButton")
        import_btn.clicked.connect(self.import_contacts)
        toolbar.addWidget(import_btn)
        
        export_btn = QPushButton("📤 导出")
        export_btn.setObjectName("secondaryButton")
        export_btn.clicked.connect(self.export_contacts)
        toolbar.addWidget(export_btn)
        
        content_layout.addLayout(toolbar)
        
        # 联系人表格
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['', '邮箱', '姓名', '分组', '互动次数', '操作'])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 40)
        self.table.setColumnWidth(5, 130)  # 加宽操作列
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        
        # 双击发送邮件
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)
        
        # 添加表头全选复选框
        self.header_checkbox = QCheckBox()
        self.header_checkbox.stateChanged.connect(self.toggle_select_all)
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.addWidget(self.header_checkbox)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.setContentsMargins(0, 0, 0, 0)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        # 将复选框放到表头第一列
        # 注意：QTableWidget的表头不支持直接setCellWidget，需要用其他方法
        # 我们改为在toolbar添加全选按钮
        
        content_layout.addWidget(self.table)
        
        # 底部批量操作栏
        self.batch_bar = QFrame()
        self.batch_bar.setVisible(False)
        
        batch_layout = QHBoxLayout(self.batch_bar)
        batch_layout.setContentsMargins(20, 12, 20, 12)
        batch_layout.setSpacing(12)
        
        self.selected_label = QLabel("已选 0 项")
        batch_layout.addWidget(self.selected_label)
        
        batch_layout.addStretch()
        
        # 复制到分组
        self.copy_combo = QComboBox()
        self.copy_combo.setMinimumWidth(140)
        self.copy_combo.setMinimumHeight(32)
        self.copy_combo.addItem("复制到分组...")
        batch_layout.addWidget(self.copy_combo)
        
        copy_btn = QPushButton("复制")
        copy_btn.setObjectName("secondaryButton")
        copy_btn.clicked.connect(self.batch_copy)
        batch_layout.addWidget(copy_btn)
        
        delete_btn = QPushButton("🗑️ 删除")
        delete_btn.setObjectName("dangerButton")
        delete_btn.clicked.connect(self.batch_delete)
        batch_layout.addWidget(delete_btn)
        
        send_btn = QPushButton("📧 发送邮件")
        send_btn.setObjectName("primaryButton")
        send_btn.setMinimumWidth(140)  # emoji + 4汉字 + padding(32px) ≈ 130px
        send_btn.adjustSize()  # 让Qt重新计算按钮最佳尺寸
        send_btn.clicked.connect(self.send_to_selected)
        batch_layout.addWidget(send_btn)
        content_layout.addWidget(self.batch_bar)
        layout.addWidget(content_panel, 1)
        
        # 应用初始主题
        self.apply_theme_styles()
    
    def update_theme(self, is_dark: bool):
        """更新主题"""
        self.is_dark_theme = is_dark
        self.apply_theme_styles()
        # 重新加载联系人以更新表格内的按钮样式
        self.load_contacts()
    
    def apply_theme_styles(self):
        """应用主题样式"""
        if self.is_dark_theme:
            # 深色主题
            self.group_panel.setStyleSheet("""
                #groupPanel {
                    background: #1E1E2E;
                    border-right: 1px solid #2D2D3D;
                }
            """)
            self.group_title.setStyleSheet("color: #9CA3AF; font-size: 12px; font-weight: 600;")
            self.add_group_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(79, 70, 229, 0.3);
                    border: none;
                    border-radius: 4px;
                    color: #A5B4FC;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: rgba(79, 70, 229, 0.5);
                }
            """)
            self.table.setStyleSheet("""
                QTableWidget {
                    background: #1A1A2E;
                    border: 1px solid #2D2D3D;
                    border-radius: 8px;
                    gridline-color: #2A2A3E;
                    alternate-background-color: #1E1E32;
                }
                QTableWidget::item {
                    padding: 10px 8px;
                    border-bottom: 1px solid #2A2A3E;
                    color: #E5E7EB;
                }
                QTableWidget::item:selected {
                    background: rgba(107, 127, 235, 0.25);
                }
                QHeaderView::section {
                    background: #15152A;
                    color: #9CA3AF;
                    padding: 12px 8px;
                    border: none;
                    border-bottom: 2px solid #2D2D3D;
                    font-weight: 600;
                    font-size: 13px;
                }
            """)
            self.batch_bar.setStyleSheet("""
                QFrame {
                    background: #252536;
                    border-radius: 8px;
                    padding: 8px;
                }
            """)
            self.selected_label.setStyleSheet("color: #A5B4FC; font-weight: 600;")
            
            # 更新分组按钮样式
            self._update_group_button_styles(True)
        else:
            # 亮色主题 - 蓝灰色调
            self.group_panel.setStyleSheet("""
                #groupPanel {
                    background: #1E293B;
                    border-right: 1px solid #334155;
                }
            """)
            self.group_title.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: 600;")
            self.add_group_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(79, 70, 229, 0.4);
                    border: none;
                    border-radius: 4px;
                    color: #C7D2FE;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: rgba(79, 70, 229, 0.6);
                }
            """)
            self.table.setStyleSheet("""
                QTableWidget {
                    background: white;
                    border: 1px solid #E2E8F0;
                    border-radius: 8px;
                    gridline-color: #E2E8F0;
                }
                QTableWidget::item {
                    padding: 8px;
                    border-bottom: 1px solid #E2E8F0;
                    color: #1E293B;
                }
                QTableWidget::item:selected {
                    background: #EEF2FF;
                    color: #1E293B;
                }
                QHeaderView::section {
                    background: #F8FAFC;
                    color: #64748B;
                    padding: 10px;
                    border: none;
                    border-bottom: 1px solid #E2E8F0;
                    font-weight: 600;
                }
            """)
            self.batch_bar.setStyleSheet("""
                QFrame {
                    background: #F1F5F9;
                    border: 1px solid #E2E8F0;
                    border-radius: 8px;
                    padding: 8px;
                }
            """)
            self.selected_label.setStyleSheet("color: #4F46E5; font-weight: 600;")
            
            # 更新分组按钮样式
            self._update_group_button_styles(False)
    
    def _update_group_button_styles(self, is_dark: bool):
        """更新所有分组按钮样式"""
        if is_dark:
            btn_style = """
                QPushButton {
                    background: transparent;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 12px;
                    text-align: left;
                    font-size: 13px;
                    color: #E5E7EB;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 0.08);
                }
                QPushButton:checked {
                    background: rgba(79, 70, 229, 0.3);
                    color: #A5B4FC;
                }
            """
        else:
            btn_style = """
                QPushButton {
                    background: transparent;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 12px;
                    text-align: left;
                    font-size: 13px;
                    color: #F1F5F9;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 0.1);
                }
                QPushButton:checked {
                    background: rgba(79, 70, 229, 0.5);
                    color: #ffffff;
                }
            """
        
        # 更新"全部联系人"按钮
        self.all_btn.setStyleSheet(btn_style)
        
        # 更新所有分组按钮
        for i in range(self.group_buttons_layout.count()):
            item = self.group_buttons_layout.itemAt(i)
            if item and item.widget():
                item.widget().setStyleSheet(btn_style)
    
    def load_data(self):
        """加载数据"""
        self.load_groups()
        self.load_contacts()
    
    def load_groups(self):
        """加载分组列表"""
        # 清空旧按钮
        while self.group_buttons_layout.count():
            item = self.group_buttons_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # 更新全部计数
        total = self.db.get_contact_count()
        self.all_btn.update_text("全部联系人", total, "📋")
        
        # 加载分组
        groups = self.db.get_groups()
        self.groups = groups
        
        # 更新复制下拉框
        self.copy_combo.clear()
        self.copy_combo.addItem("复制到分组...", None)
        
        for g in groups:
            btn = GroupButton(
                g['name'], g['contact_count'], g['icon'], 
                g['color'], g['id']
            )
            btn.clicked.connect(lambda checked, gid=g['id']: self.select_group(gid))
            
            # 右键菜单
            btn.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            btn.customContextMenuRequested.connect(
                lambda pos, b=btn: self.show_group_menu(b, pos)
            )
            
            self.group_buttons_layout.addWidget(btn)
            self.copy_combo.addItem(f"{g['icon']}  {g['name']}", g['id'])
    
    def load_contacts(self):
        """加载联系人列表"""
        search = self.search_input.text().strip()
        contacts = self.db.get_contacts(group_id=self.current_group_id, search=search)
        
        self.table.setRowCount(len(contacts))
        
        # 重置全选复选框状态
        self.select_all_checkbox.blockSignals(True)
        self.select_all_checkbox.setChecked(False)
        self.select_all_checkbox.blockSignals(False)
        
        for row, c in enumerate(contacts):
            # 复选框
            cb = QCheckBox()
            cb.setProperty('contact_id', c['id'])
            cb.stateChanged.connect(self.on_selection_changed)
            
            cb_widget = QWidget()
            cb_layout = QHBoxLayout(cb_widget)
            cb_layout.addWidget(cb)
            cb_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cb_layout.setContentsMargins(0, 0, 0, 0)
            self.table.setCellWidget(row, 0, cb_widget)
            
            # 邮箱（添加tooltip显示完整地址）
            email_text = c['email']
            if len(email_text) > 20:
                display_email = email_text[:17] + '...'
            else:
                display_email = email_text
            email_item = QTableWidgetItem(display_email)
            email_item.setData(Qt.ItemDataRole.UserRole, c['id'])
            email_item.setToolTip(f"完整邮箱：{email_text}")  # 添加tooltip
            self.table.setItem(row, 1, email_item)
            
            # 姓名（无姓名时显示提示文字）
            name_text = c['name'] if c['name'] else '无姓名数据'
            name_item = QTableWidgetItem(name_text)
            if not c['name']:
                name_item.setForeground(QBrush(QColor('#6B7280')))  # 灰色提示
            self.table.setItem(row, 2, name_item)
            
            # 分组
            group_text = c['group_name'] or '未分组'
            group_item = QTableWidgetItem(group_text)
            if c['group_color']:
                group_item.setForeground(QBrush(QColor(c['group_color'])))
            self.table.setItem(row, 3, group_item)
            
            # 互动次数（用强调色）
            count_item = QTableWidgetItem(str(c['interaction_count']))
            count_item.setForeground(QBrush(QColor('#10B981')))  # 绿色强调
            self.table.setItem(row, 4, count_item)
            
            # 操作按钮
            ops_widget = QWidget()
            ops_layout = QHBoxLayout(ops_widget)
            ops_layout.setContentsMargins(4, 4, 4, 4)
            ops_layout.setSpacing(4)
            
            edit_btn = QPushButton("✏️")
            edit_btn.setFixedSize(28, 28)
            edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            edit_btn.setToolTip("编辑联系人")
            if self.is_dark_theme:
                edit_btn.setStyleSheet("""
                    QPushButton {
                        background: rgba(107, 127, 235, 0.15);
                        border: 1px solid rgba(107, 127, 235, 0.3);
                        border-radius: 4px;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background: rgba(107, 127, 235, 0.35);
                        border-color: rgba(107, 127, 235, 0.5);
                    }
                """)
            else:
                edit_btn.setStyleSheet("""
                    QPushButton {
                        background: rgba(79, 70, 229, 0.1);
                        border: 1px solid rgba(79, 70, 229, 0.2);
                        border-radius: 4px;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background: rgba(79, 70, 229, 0.25);
                        border-color: rgba(79, 70, 229, 0.4);
                    }
                """)
            edit_btn.clicked.connect(lambda checked, cid=c['id']: self.edit_contact(cid))
            ops_layout.addWidget(edit_btn)
            
            del_btn = QPushButton("🗑️")
            del_btn.setFixedSize(28, 28)
            del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            del_btn.setToolTip("删除联系人")
            del_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(239, 68, 68, 0.15);
                    border: 1px solid rgba(239, 68, 68, 0.3);
                    border-radius: 4px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background: rgba(239, 68, 68, 0.35);
                    border-color: rgba(239, 68, 68, 0.5);
                }
            """)
            del_btn.clicked.connect(lambda checked, cid=c['id']: self.delete_contact(cid))
            ops_layout.addWidget(del_btn)
            
            # 快捷发送按钮
            send_btn = QPushButton("📧")
            send_btn.setFixedSize(28, 28)
            send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            send_btn.setToolTip("快捷发送邮件")
            send_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(16, 185, 129, 0.15);
                    border: 1px solid rgba(16, 185, 129, 0.3);
                    border-radius: 4px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background: rgba(16, 185, 129, 0.35);
                    border-color: rgba(16, 185, 129, 0.5);
                }
            """)
            contact_data = {'id': c['id'], 'email': c['email'], 'name': c['name']}
            send_btn.clicked.connect(lambda checked, cd=contact_data: self.quick_send(cd))
            ops_layout.addWidget(send_btn)
            
            self.table.setCellWidget(row, 5, ops_widget)
        
        self.update_selection_state()
    
    def on_cell_double_clicked(self, row: int, col: int):
        """双击单元格 - 打开快捷发送"""
        if col == 0 or col == 5:  # 复选框列和操作列不响应
            return
        
        email_item = self.table.item(row, 1)
        if email_item:
            contact_id = email_item.data(Qt.ItemDataRole.UserRole)
            contacts = self.db.get_contacts()
            contact = next((c for c in contacts if c['id'] == contact_id), None)
            if contact:
                self.quick_send({'id': contact['id'], 'email': contact['email'], 'name': contact['name']})
    
    def quick_send(self, contact: dict):
        """快捷发送邮件"""
        self.quick_send_requested.emit(contact)
    
    def select_group(self, group_id):
        """选择分组"""
        self.current_group_id = group_id
        
        # 更新按钮状态
        self.all_btn.setChecked(group_id is None)
        
        for i in range(self.group_buttons_layout.count()):
            btn = self.group_buttons_layout.itemAt(i).widget()
            if isinstance(btn, GroupButton):
                btn.setChecked(btn.group_id == group_id)
        
        self.load_contacts()
    
    def on_search(self):
        """搜索"""
        self.load_contacts()
    
    def on_selection_changed(self):
        """选择变化"""
        self.update_selection_state()
        # 同步全选复选框状态
        self.sync_select_all_checkbox()
    
    def update_selection_state(self):
        """更新选择状态"""
        selected = []
        for row in range(self.table.rowCount()):
            cb_widget = self.table.cellWidget(row, 0)
            if cb_widget:
                cb = cb_widget.findChild(QCheckBox)
                if cb and cb.isChecked():
                    contact_id = cb.property('contact_id')
                    selected.append(contact_id)
        
        self.selected_contacts = selected
        self.selected_label.setText(f"已选 {len(selected)} 项")
        self.batch_bar.setVisible(len(selected) > 0)
    
    def toggle_select_all(self, state):
        """全选/取消全选 - 只影响当前显示的行（搜索后也准确）"""
        checked = (state == Qt.CheckState.Checked.value)
        
        # 遍历当前表格中所有显示的行
        for row in range(self.table.rowCount()):
            cb_widget = self.table.cellWidget(row, 0)
            if cb_widget:
                cb = cb_widget.findChild(QCheckBox)
                if cb:
                    # 临时断开信号避免触发大量update
                    cb.blockSignals(True)
                    cb.setChecked(checked)
                    cb.blockSignals(False)
        
        # 统一触发一次更新
        self.update_selection_state()
    
    def sync_select_all_checkbox(self):
        """同步全选复选框状态"""
        if self.table.rowCount() == 0:
            self.select_all_checkbox.setChecked(False)
            return
        
        # 检查是否所有当前显示的行都被选中
        all_checked = True
        for row in range(self.table.rowCount()):
            cb_widget = self.table.cellWidget(row, 0)
            if cb_widget:
                cb = cb_widget.findChild(QCheckBox)
                if cb and not cb.isChecked():
                    all_checked = False
                    break
        
        # 更新全选复选框状态（避免触发toggle_select_all）
        self.select_all_checkbox.blockSignals(True)
        self.select_all_checkbox.setChecked(all_checked)
        self.select_all_checkbox.blockSignals(False)
    
    def add_group(self):
        """添加分组"""
        dialog = GroupEditDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data['name']:
                try:
                    self.db.create_group(data['name'], icon=data['icon'])
                    self.load_groups()
                except Exception as e:
                    QMessageBox.warning(self, "错误", f"创建分组失败: {e}")
    
    def show_group_menu(self, btn: GroupButton, pos):
        """显示分组右键菜单"""
        menu = QMenu(self)
        
        rename_action = QAction("✏️ 重命名", self)
        rename_action.triggered.connect(lambda: self.rename_group(btn))
        menu.addAction(rename_action)
        
        delete_action = QAction("🗑️ 删除分组", self)
        delete_action.triggered.connect(lambda: self.delete_group(btn))
        menu.addAction(delete_action)
        
        menu.exec(btn.mapToGlobal(pos))
    
    def rename_group(self, btn: GroupButton):
        """重命名分组"""
        groups = [g for g in self.groups if g['id'] == btn.group_id]
        if not groups:
            return
        
        dialog = GroupEditDialog(group=groups[0], parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data['name']:
                self.db.rename_group(btn.group_id, data['name'])
                self.load_groups()
    
    def delete_group(self, btn: GroupButton):
        """删除分组"""
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除分组「{btn.group_name}」吗？\n\n该分组下的联系人将变为未分组。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_group(btn.group_id)
            if self.current_group_id == btn.group_id:
                self.current_group_id = None
            self.load_data()
    
    def add_contact(self):
        """添加联系人"""
        dialog = ContactEditDialog(groups=self.groups, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data['email']:
                self.db.add_contact(
                    email=data['email'],
                    name=data['name'],
                    group_id=data['group_id']
                )
                if data['notes']:
                    contacts = self.db.get_contacts(search=data['email'])
                    if contacts:
                        self.db.update_contact(contacts[0]['id'], notes=data['notes'])
                self.load_data()
    
    def edit_contact(self, contact_id: int):
        """编辑联系人"""
        contacts = self.db.get_contacts()
        contact = next((c for c in contacts if c['id'] == contact_id), None)
        if not contact:
            return
        
        dialog = ContactEditDialog(contact=contact, groups=self.groups, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            self.db.update_contact(
                contact_id,
                name=data['name'],
                group_id=data['group_id'],
                notes=data['notes']
            )
            self.load_data()
    
    def delete_contact(self, contact_id: int):
        """删除联系人 - 提供两个选项"""
        # 创建自定义对话框
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("删除选项")
        msg_box.setText("请选择删除方式：")
        
        # 如果在特定分组中，提供"从当前分组移除"选项
        if self.current_group_id is not None:
            msg_box.setInformativeText(
                "• 从当前分组移除：联系人仍保留在数据库中\n"
                "• 彻底删除：完全从数据库删除该联系人"
            )
            remove_btn = msg_box.addButton("从当前分组移除", QMessageBox.ButtonRole.ActionRole)
            delete_btn = msg_box.addButton("彻底删除", QMessageBox.ButtonRole.DestructiveRole)
            msg_box.addButton("取消", QMessageBox.ButtonRole.RejectRole)
            
            msg_box.exec()
            clicked = msg_box.clickedButton()
            
            if clicked == remove_btn:
                # 从当前分组移除（使用新的remove方法）
                self.db.remove_contacts_from_group([contact_id], self.current_group_id)
                self.load_data()
            elif clicked == delete_btn:
                # 彻底删除
                self.db.delete_contact(contact_id)
                self.load_data()
        else:
            # 在"全部联系人"视图，只提供彻底删除
            reply = QMessageBox.question(
                self, "确认删除",
                "确定要彻底删除这个联系人吗？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.db.delete_contact(contact_id)
                self.load_data()
    
    def batch_copy(self):
        """批量复制到分组"""
        if not self.selected_contacts:
            return
        
        group_id = self.copy_combo.currentData()
        group_name = self.copy_combo.currentText()
        
        # 验证选择
        if group_id is None or group_name == "复制到分组...":
            QMessageBox.warning(self, "提示", "请选择目标分组")
            return
        
        # 复制联系人到指定分组（不影响原有分组）
        self.db.copy_contacts_to_group(self.selected_contacts, group_id)
        self.load_data()
        
        # 提示用户
        count = len(self.selected_contacts)
        QMessageBox.information(self, "操作成功", f"已将 {count} 个联系人复制到「{group_name}」")
    
    def batch_delete(self):
        """批量删除 - 提供两个选项"""
        if not self.selected_contacts:
            return
        
        count = len(self.selected_contacts)
        
        # 创建自定义对话框
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("删除选项")
        msg_box.setText(f"请选择删除方式：已选中 {count} 个联系人")
        
        # 如果在特定分组中，提供"从当前分组移除"选项
        if self.current_group_id is not None:
            msg_box.setInformativeText(
                "• 从当前分组移除：联系人仍保留在数据库中\n"
                "• 彻底删除：完全从数据库删除这些联系人"
            )
            remove_btn = msg_box.addButton("从当前分组移除", QMessageBox.ButtonRole.ActionRole)
            delete_btn = msg_box.addButton("彻底删除", QMessageBox.ButtonRole.DestructiveRole)
            msg_box.addButton("取消", QMessageBox.ButtonRole.RejectRole)
            
            msg_box.exec()
            clicked = msg_box.clickedButton()
            
            if clicked == remove_btn:
                # 从当前分组移除（使用新的remove_contacts_from_group方法）
                self.db.remove_contacts_from_group(self.selected_contacts, self.current_group_id)
                self.load_data()
                QMessageBox.information(self, "操作成功", f"已将 {count} 个联系人从当前分组移除")
            elif clicked == delete_btn:
                # 彻底删除
                self.db.delete_contacts(self.selected_contacts)
                self.load_data()
                QMessageBox.information(self, "操作成功", f"已彻底删除 {count} 个联系人")
        else:
            # 在"全部联系人"视图，只提供彻底删除
            reply = QMessageBox.question(
                self, "确认删除",
                f"确定要彻底删除选中的 {count} 个联系人吗？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.db.delete_contacts(self.selected_contacts)
                self.load_data()
                QMessageBox.information(self, "操作成功", f"已彻底删除 {count} 个联系人")
    
    def send_to_selected(self):
        """发送邮件到选中联系人"""
        if not self.selected_contacts:
            return
        
        contacts = []
        for cid in self.selected_contacts:
            all_contacts = self.db.get_contacts()
            c = next((x for x in all_contacts if x['id'] == cid), None)
            if c:
                contacts.append({'email': c['email'], 'name': c['name']})
        
        self.contacts_selected_for_send.emit(contacts)
    
    def import_contacts(self):
        """导入联系人"""
        path, _ = QFileDialog.getOpenFileName(
            self, "选择文件", "",
            "CSV文件 (*.csv);;文本文件 (*.txt);;所有文件 (*.*)"
        )
        
        if not path:
            return
        
        try:
            contacts = []
            if path.endswith('.csv'):
                import csv
                with open(path, 'r', encoding='utf-8-sig') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        email = row.get('邮箱') or row.get('email') or row.get('Email', '')
                        name = row.get('姓名') or row.get('name') or row.get('Name', '')
                        if email:
                            contacts.append({'email': email.strip(), 'name': name.strip()})
            else:
                with open(path, 'r', encoding='utf-8') as f:
                    for line in f:
                        email = line.strip()
                        if email and '@' in email:
                            contacts.append({'email': email, 'name': ''})
            
            if contacts:
                count = self.db.import_contacts(contacts, group_id=self.current_group_id)
                QMessageBox.information(self, "导入成功", f"成功导入 {count} 个联系人")
                self.load_data()
            else:
                QMessageBox.warning(self, "导入失败", "未找到有效的联系人数据")
        except Exception as e:
            QMessageBox.critical(self, "导入失败", f"导入失败: {e}")
    
    def export_contacts(self):
        """导出联系人"""
        contacts = self.db.get_contacts(group_id=self.current_group_id)
        if not contacts:
            QMessageBox.warning(self, "无数据", "当前没有可导出的联系人")
            return
        
        path, _ = QFileDialog.getSaveFileName(
            self, "导出联系人", "",
            "CSV文件 (*.csv);;文本文件 (*.txt)"
        )
        
        if not path:
            return
        
        try:
            if path.endswith('.csv'):
                import csv
                with open(path, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(['邮箱', '姓名', '分组', '互动次数', '备注'])
                    for c in contacts:
                        writer.writerow([
                            c['email'], c['name'], c['group_name'] or '',
                            c['interaction_count'], c.get('notes', '')
                        ])
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    for c in contacts:
                        f.write(c['email'] + '\n')
            
            QMessageBox.information(self, "导出成功", f"成功导出 {len(contacts)} 个联系人")
        except Exception as e:
            QMessageBox.critical(self, "导出失败", f"导出失败: {e}")
    
    def save_fetched_contacts(self, contacts: list, group_id: int = None):
        """保存采集到的联系人"""
        count = self.db.import_contacts(contacts, group_id=group_id)
        self.load_data()
        return count
