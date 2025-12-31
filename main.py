#!/usr/bin/env python3
"""
Eason - 邮件批量发送助手 v2.0
模块化重构版本

使用方法:
    python main.py
"""
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from src.ui import MainWindow


def main():
    """主入口"""
    app = QApplication(sys.argv)
    app.setApplicationName("Eason")
    app.setOrganizationName("EmailAssistant")
    
    # 设置全局字体，确保中文显示正常
    font = QFont()
    font.setFamily("PingFang SC")  # macOS 中文字体
    font.setPointSize(13)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
