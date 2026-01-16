
content = r'''"""
极客紫样式系统 - Purple Geek Theme (Deep Nebula)
Work is Art.
"""

PURPLE_THEME = """
/* ============================================
   全局基础
   ============================================ */
QMainWindow, QWidget {
    background-color: #0F0F1A;  /* Deep Space Black/Purple */
    color: #E0E0E0;
    font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
}

QFrame#contentArea {
    background-color: #0F0F1A;
}

/* ============================================
   侧边栏 (Level 2)
   ============================================ */
QFrame#sidebar {
    background-color: #181828;
    border-right: 1px solid #1F1F33;
}

QLabel#logoText {
    color: #FFFFFF;
    font-family: 'Segoe UI', sans-serif;
    font-size: 24px;
    font-weight: 800;
    letter-spacing: 1px;
}

/* 侧边栏按钮 */
QPushButton {
    text-align: left;
    padding-left: 20px;
    font-size: 14px;
    color: #A0A0B0;
    border: none;
    background-color: transparent;
    border-radius: 12px;
    margin: 4px 12px;
}

QPushButton:hover {
    background-color: #232336;
    color: #FFFFFF;
}

QPushButton:checked {
    background-color: #6C5CE7; /* Active Purple */
    color: #FFFFFF;
    font-weight: 600;
}

/* ============================================
   卡片与容器 (Level 3)
   ============================================ */
QFrame#bannerCard, QGroupBox, QFrame[objectName^="statsCard"] {
    background-color: #232336;
    border-radius: 16px;
    border: 1px solid #2D2D44; /* Subtle border */
}

QGroupBox {
    margin-top: 24px;
    padding: 24px;
    font-weight: 600;
    color: #FFFFFF;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    color: #A0A0B0;
    font-size: 14px;
}

/* ============================================
   字体排版
   ============================================ */
QLabel#pageTitle {
    color: #FFFFFF;
    font-size: 28px;
    font-weight: 700;
}

QLabel#bannerTitle {
    color: #FFFFFF;
    font-size: 20px;
    font-weight: 700;
}

QLabel#bannerSubtitle {
    color: #A0A0B0;
    font-size: 14px;
}

QLabel {
    color: #E0E0E0;
}

QLabel#fieldLabel, QLabel#settingLabel {
    color: #A0A0B0;
    font-size: 13px;
    font-weight: 500;
}

/* ============================================
   输入框 (Level 4 - Deep)
   ============================================ */
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox {
    background-color: #151520; /* Deep inset */
    border: 1px solid #2D2D44;
    border-radius: 12px;
    padding: 10px 14px;
    color: #FFFFFF;
    font-size: 14px;
    selection-background-color: #6C5CE7;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus {
    border: 1px solid #6C5CE7;
    background-color: #1A1A26;
}

/* Placeholder color */
QLineEdit::placeholder, QTextEdit::placeholder {
    color: #555566;
}

/* ============================================
   按钮系统
   ============================================ */
QPushButton#primaryButton {
    background-color: #6C5CE7;
    color: white;
    border-radius: 12px;
    padding: 10px 24px;
    font-weight: 600;
    text-align: center;
}

QPushButton#primaryButton:hover {
    background-color: #5B4BC4;
    border: 1px solid #7D6EF0;
}

QPushButton#primaryButton:pressed {
    background-color: #4A3DB0;
}

QPushButton#secondaryButton {
    background-color: rgba(255, 255, 255, 0.05); /* Glassy white */
    color: #E0E0E0;
    border: 1px solid #2D2D44;
    border-radius: 12px;
    padding: 8px 16px;
    text-align: center;
}

QPushButton#secondaryButton:hover {
    background-color: rgba(255, 255, 255, 0.1);
    color: #FFFFFF;
}

QPushButton#dangerButton {
    background-color: rgba(231, 76, 60, 0.15);
    color: #FF6B6B;
    border: 1px solid rgba(231, 76, 60, 0.3);
    border-radius: 12px;
    text-align: center;
}

QPushButton#dangerButton:hover {
    background-color: rgba(231, 76, 60, 0.25);
    border-color: #FF6B6B;
}

/* ============================================
   表格与列表
   ============================================ */
QTableWidget {
    background-color: #232336;
    border: 1px solid #2D2D44;
    border-radius: 12px;
    gridline-color: #2D2D44;
    color: #E0E0E0;
    selection-background-color: rgba(108, 92, 231, 0.2);
    selection-color: #FFFFFF;
}

QHeaderView::section {
    background-color: #1F1F33;
    color: #A0A0B0;
    padding: 8px;
    border: none;
    border-bottom: 2px solid #2D2D44;
    font-weight: 600;
}

QTableWidget::item {
    padding: 5px;
}

/* ============================================
   其他组件
   ============================================ */
QProgressBar {
    background-color: #151520;
    border-radius: 6px;
    text-align: center;
    color: #FFFFFF;
    font-size: 12px;
}

QProgressBar::chunk {
    background-color: #6C5CE7;
    border-radius: 6px;
}

QComboBox {
    background-color: #151520;
    border: 1px solid #2D2D44;
    border-radius: 12px;
    padding: 8px 12px;
    color: #FFFFFF;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #6C5CE7;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #232336;
    border: 1px solid #2D2D44;
    selection-background-color: #6C5CE7;
    color: white;
    outline: none;
}

/* 滚动条 - 极简 */
QScrollBar:vertical {
    border: none;
    background: transparent;
    width: 8px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #444455;
    min-height: 20px;
    border-radius: 4px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""
'''
with open('/Users/code/Eason/src/ui/styles_premium.py', 'w') as f:
    f.write(content)
print("Updated styles_premium.py")
