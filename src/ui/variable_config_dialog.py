"""
变量配置对话框
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit,
                             QDialogButtonBox, QLabel, QScrollArea, QWidget)
from PyQt6.QtCore import Qt
from typing import Dict


class VariableConfigDialog(QDialog):
    """变量配置对话框"""
    
    def __init__(self, current_vars: Dict, required_vars: list = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⚙️ 配置模板变量")
        self.setMinimumSize(500, 450)
        
        main_layout = QVBoxLayout(self)
        
        # 提示信息
        info_text = "配置邮件模板中的变量值"
        if required_vars:
            info_text += "\n必填变量标记为 *"
        info = QLabel(info_text)
        info.setStyleSheet("color: #666; padding: 10px; background: #e3f2fd; border-radius: 5px;")
        main_layout.addWidget(info)
        
        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        
        scroll_widget = QWidget()
        form_layout = QFormLayout(scroll_widget)
        form_layout.setSpacing(15)
        
        # 变量输入框
        self.inputs = {}
        
        # 发件人信息
        is_required = 'sender_name' in (required_vars or [])
        label = "* 发件人姓名:" if is_required else "发件人姓名:"
        self.inputs['sender_name'] = QLineEdit(current_vars.get('sender_name', ''))
        self.inputs['sender_name'].setPlaceholderText("显示在邮件签名中")
        form_layout.addRow(label, self.inputs['sender_name'])
        
        is_required = 'sender_company' in (required_vars or [])
        label = "* 发件人公司:" if is_required else "发件人公司:"
        self.inputs['sender_company'] = QLineEdit(current_vars.get('sender_company', ''))
        self.inputs['sender_company'].setPlaceholderText("您的公司或组织名称")
        form_layout.addRow(label, self.inputs['sender_company'])
        
        # 自定义字段
        for i in range(1, 4):
            key = f'custom_{i}'
            self.inputs[key] = QLineEdit(current_vars.get(key, ''))
            self.inputs[key].setPlaceholderText(f"可用于活动时间、地点、链接等")
            form_layout.addRow(f"自定义字段{i}:", self.inputs[key])
        
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        
        # 按钮
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        main_layout.addWidget(buttons)
        
        # 样式
        self.setStyleSheet("""
            QDialog {
                background: white;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #2196F3;
            }
        """)
    
    def get_variables(self) -> Dict:
        """获取配置的变量"""
        return {
            key: input_widget.text().strip()
            for key, input_widget in self.inputs.items()
        }
