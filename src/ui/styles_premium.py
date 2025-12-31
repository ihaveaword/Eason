"""
极简主义样式系统 - Minimalist Design
参考: Vercel, Linear, Arc Browser
"""

LIGHT_THEME_PREMIUM = """
/* ============================================
   全局样式 - 极简主义
   ============================================ */
QMainWindow {
    background-color: #fafafa;
}

/* ============================================
   卡片样式 - 极简无边框
   ============================================ */
QGroupBox {
    font-weight: 500;
    font-size: 13px;
    border: 1px solid #e5e5e5;
    border-radius: 8px;
    margin-top: 8px;
    padding: 20px;
    background-color: white;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: #171717;
    font-size: 14px;
    font-weight: 600;
}

/* ============================================
   统计卡片 - 极简设计
   ============================================ */
QFrame[objectName="statsCard"] {
    background-color: white;
    border: 1px solid #e5e5e5;
    border-radius: 8px;
}

QFrame[objectName="statsCardSuccess"] {
    background-color: white;
    border: 1px solid #e5e5e5;
    border-radius: 8px;
}

QFrame[objectName="statsCardInfo"] {
    background-color: white;
    border: 1px solid #e5e5e5;
    border-radius: 8px;
}

QFrame[objectName="statsCardWarning"] {
    background-color: white;
    border: 1px solid #e5e5e5;
    border-radius: 8px;
}

/* ============================================
   按钮系统 - 极简克制
   ============================================ */
QPushButton {
    background-color: #171717;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 18px;
    font-weight: 500;
    font-size: 13px;
    min-height: 32px;
}

QPushButton:hover {
    background-color: #404040;
}

QPushButton:pressed {
    background-color: #0a0a0a;
}

QPushButton:disabled {
    background-color: #fafafa;
    color: #a3a3a3;
    border: 1px solid #e5e5e5;
}

/* 成功按钮 */
QPushButton#successButton {
    background-color: #18181b;
    color: white;
}

QPushButton#successButton:hover {
    background-color: #27272a;
}

/* 停止按钮 */
QPushButton#stopButton {
    background-color: #dc2626;
    color: white;
}

QPushButton#stopButton:hover {
    background-color: #ef4444;
}

/* 次要按钮 */
QPushButton#secondaryButton {
    background-color: white;
    color: #171717;
    border: 1px solid #e5e5e5;
}

QPushButton#secondaryButton:hover {
    background-color: #fafafa;
    border-color: #d4d4d4;
}

/* 主题切换按钮 */
QPushButton#themeButton {
    background-color: #f5f5f5;
    color: #171717;
    border: 1px solid #e5e5e5;
    min-width: 100px;
    border-radius: 6px;
    padding: 8px 14px;
}

QPushButton#themeButton:hover {
    background-color: #e5e5e5;
}

/* ============================================
   输入框样式 - 极简
   ============================================ */
QLineEdit, QTextEdit, QSpinBox {
    border: 1px solid #e5e5e5;
    border-radius: 6px;
    padding: 8px 12px;
    background-color: white;
    color: #171717;
    font-size: 13px;
    selection-background-color: #171717;
    selection-color: white;
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus {
    border: 1px solid #171717;
    background-color: white;
}

QLineEdit:hover, QTextEdit:hover, QSpinBox:hover {
    border-color: #d4d4d4;
}

/* ============================================
   下拉框样式
   ============================================ */
QComboBox {
    border: 1px solid #e5e5e5;
    border-radius: 6px;
    padding: 8px 12px;
    background-color: white;
    color: #171717;
    font-size: 13px;
    min-height: 32px;
}

QComboBox:hover {
    border-color: #d4d4d4;
}

QComboBox:focus {
    border: 1px solid #171717;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #737373;
    margin-right: 6px;
}

QComboBox QAbstractItemView {
    background-color: white;
    border: 1px solid #e5e5e5;
    border-radius: 6px;
    selection-background-color: #f5f5f5;
    selection-color: #171717;
    padding: 4px;
}

/* ============================================
   进度条样式 - 极简
   ============================================ */
QProgressBar {
    border: none;
    border-radius: 4px;
    text-align: center;
    background-color: #f5f5f5;
    color: #171717;
    height: 24px;
    font-weight: 500;
    font-size: 12px;
}

QProgressBar::chunk {
    background-color: #171717;
    border-radius: 4px;
}

/* ============================================
   标签样式 - 排版驱动
   ============================================ */
QLabel {
    color: #171717;
    font-size: 13px;
}

QLabel[objectName="statValue"] {
    color: #171717;
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.5px;
}

QLabel[objectName="statLabel"] {
    color: #737373;
    font-size: 12px;
    font-weight: 500;
}

/* ============================================
   标签页样式 - 无边框美学
   ============================================ */
QTabWidget::pane {
    border: 1px solid #e5e5e5;
    border-radius: 8px;
    background-color: white;
    padding: 16px;
}

QTabBar::tab {
    background-color: transparent;
    color: #737373;
    padding: 10px 20px;
    margin-right: 4px;
    border: none;
    border-bottom: 2px solid transparent;
    font-size: 13px;
    font-weight: 500;
}

QTabBar::tab:selected {
    color: #171717;
    border-bottom: 2px solid #171717;
    font-weight: 600;
}

QTabBar::tab:hover:!selected {
    color: #404040;
}

/* ============================================
   复选框样式
   ============================================ */
QCheckBox {
    color: #171717;
    font-size: 13px;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid #e5e5e5;
    border-radius: 4px;
    background-color: white;
}

QCheckBox::indicator:hover {
    border-color: #171717;
}

QCheckBox::indicator:checked {
    background-color: #171717;
    border-color: #171717;
}

/* ============================================
   滚动条样式 - 极简
   ============================================ */
QScrollBar:vertical {
    background: #fafafa;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #d4d4d4;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #a3a3a3;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""

# 暗色主题 - 极简主义
DARK_THEME_PREMIUM = """
/* 全局 - 极简暗色 */
QMainWindow {
    background-color: #0a0a0a;
}

QGroupBox {
    font-weight: 500;
    font-size: 13px;
    border: 1px solid #262626;
    border-radius: 8px;
    margin-top: 8px;
    padding: 20px;
    background-color: #171717;
    color: #fafafa;
}

QGroupBox::title {
    color: #fafafa;
    font-size: 14px;
    font-weight: 600;
}

QFrame[objectName="statsCard"], 
QFrame[objectName="statsCardSuccess"],
QFrame[objectName="statsCardInfo"],
QFrame[objectName="statsCardWarning"] {
    background-color: #171717;
    border: 1px solid #262626;
    border-radius: 8px;
}

QPushButton {
    background-color: #fafafa;
    color: #0a0a0a;
    border: none;
    border-radius: 6px;
    padding: 10px 18px;
    font-weight: 500;
    font-size: 13px;
    min-height: 32px;
}

QPushButton:hover {
    background-color: #e5e5e5;
}

QPushButton#stopButton {
    background-color: #dc2626;
    color: white;
}

QPushButton#secondaryButton {
    background-color: #171717;
    color: #fafafa;
    border: 1px solid #262626;
}

QPushButton#themeButton {
    background-color: #262626;
    color: #fafafa;
    border: 1px solid #404040;
}

QLineEdit, QTextEdit, QSpinBox {
    border: 1px solid #262626;
    border-radius: 6px;
    padding: 8px 12px;
    background-color: #171717;
    color: #fafafa;
    font-size: 13px;
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus {
    border: 1px solid #fafafa;
}

QComboBox {
    border: 1px solid #262626;
    border-radius: 6px;
    background-color: #171717;
    color: #fafafa;
    font-size: 13px;
}

QComboBox QAbstractItemView {
    background-color: #171717;
    border: 1px solid #262626;
    color: #fafafa;
    selection-background-color: #262626;
}

QProgressBar {
    border: none;
    border-radius: 4px;
    background-color: #262626;
    color: #fafafa;
    height: 24px;
    font-weight: 500;
}

QProgressBar::chunk {
    background-color: #fafafa;
    border-radius: 4px;
}

QLabel {
    color: #fafafa;
    font-size: 13px;
}

QLabel[objectName="statValue"] {
    color: #fafafa;
    font-size: 28px;
    font-weight: 700;
}

QLabel[objectName="statLabel"] {
    color: #737373;
    font-size: 12px;
    font-weight: 500;
}

QTabWidget::pane {
    border: 1px solid #262626;
    border-radius: 8px;
    background-color: #171717;
    padding: 16px;
}

QTabBar::tab {
    background-color: transparent;
    color: #737373;
    padding: 10px 20px;
    border: none;
    border-bottom: 2px solid transparent;
}

QTabBar::tab:selected {
    color: #fafafa;
    border-bottom: 2px solid #fafafa;
    font-weight: 600;
}

QCheckBox {
    color: #fafafa;
}

QCheckBox::indicator {
    border: 1px solid #262626;
    background-color: #171717;
}

QCheckBox::indicator:checked {
    background-color: #fafafa;
    border-color: #fafafa;
}

QScrollBar:vertical {
    background: #0a0a0a;
    width: 8px;
}

QScrollBar::handle:vertical {
    background: #404040;
    border-radius: 4px;
}
"""
