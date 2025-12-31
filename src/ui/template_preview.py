"""
模板预览对话框
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QTextBrowser, 
                             QDialogButtonBox, QLabel)
from PyQt6.QtCore import Qt


class TemplatePreviewDialog(QDialog):
    """模板预览对话框"""
    
    def __init__(self, html_content: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📧 邮件模板预览")
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(self)
        
        # 提示信息
        info = QLabel("预览效果（实际邮件可能因邮箱客户端而略有差异）")
        info.setStyleSheet("color: #666; padding: 10px; background: #f5f5f5; border-radius: 5px;")
        layout.addWidget(info)
        
        # HTML预览控件
        self.browser = QTextBrowser()
        self.browser.setHtml(html_content)
        self.browser.setOpenExternalLinks(False)
        layout.addWidget(self.browser)
        
        # 按钮
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)
        
        # 样式
        self.setStyleSheet("""
            QDialog {
                background: white;
            }
            QTextBrowser {
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
