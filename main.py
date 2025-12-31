#!/usr/bin/env python3
"""
Eason - 邮件批量发送助手 v2.0
模块化重构版本

使用方法:
    python main.py
"""
import sys
from PyQt6.QtWidgets import QApplication
from src.ui import MainWindow


def main():
    """主入口"""
    app = QApplication(sys.argv)
    app.setApplicationName("Eason")
    app.setOrganizationName("EmailAssistant")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
