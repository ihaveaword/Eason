"""
极客紫样式系统 - Purple Geek Theme (Deep Nebula)
Work is Art.
"""

PURPLE_THEME = """
/* ============================================
   全局基础
   ============================================ */
QMainWindow, QWidget {
    background-color: #1C1E2E;  /* Blue-gray main bg */
    color: #E0E4F0;
    font-family: 'PingFang SC', 'Helvetica Neue', 'Microsoft YaHei', sans-serif;
}

QFrame#contentArea {
    background-color: #1C1E2E;
}

/* ============================================
   侧边栏 (Level 2)
   ============================================ */
QFrame#sidebar {
    background-color: #141621;
    border-right: 1px solid #252838;
}

QLabel#logoText {
    color: #FFFFFF;
    font-family: -apple-system, 'PingFang SC', 'Helvetica Neue', sans-serif;
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
    background-color: #6B7FEB; /* Active Blue-Purple from icon */
    color: #FFFFFF;
    font-weight: 600;
}

/* ============================================
   卡片与容器 (Level 3)
   ============================================ */
QFrame#bannerCard, QGroupBox, QFrame#statsCard, QFrame#statusCard, QFrame#contentCard {
    background-color: #242738;
    border-radius: 16px;
    border: none; /* 无边框，更融合 */
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
    background: transparent;
}

QLabel#fieldLabel, QLabel#settingLabel {
    color: #A0A0B0;
    font-size: 13px;
    font-weight: 500;
    background: transparent;
}

/* 卡片内的标签样式 */
QLabel#cardIcon {
    background: transparent;
    font-size: 20px;
}

QLabel#cardTitle {
    color: #A0A0B0;
    font-size: 13px;
    font-weight: 500;
    background: transparent;
}

QLabel#cardValue {
    color: #FFFFFF;
    font-size: 28px;
    font-weight: 700;
    background: transparent;
}

QLabel#cardSubtitle {
    color: #6B7280;
    font-size: 12px;
    background: transparent;
}

QLabel#sectionTitle {
    color: #FFFFFF;
    font-size: 16px;
    font-weight: 600;
    background: transparent;
}

QLabel#tipLabel {
    color: #6B7280;
    font-size: 12px;
    background: transparent;
}

QLabel#statValue {
    color: #FFFFFF;
    font-size: 24px;
    font-weight: 700;
    background: transparent;
}

/* ============================================
   输入框 (Level 4 - Deep)
   ============================================ */
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox {
    background-color: #171925; /* Deep inset */
    border: 1px solid #2D2F44;
    border-radius: 12px;
    padding: 10px 14px;
    color: #FFFFFF;
    font-size: 14px;
    selection-background-color: #6B7FEB;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus {
    border: 1px solid #6B7FEB;
    background-color: #1E202E;
}

/* Placeholder color */
QLineEdit::placeholder, QTextEdit::placeholder {
    color: #555566;
}

/* ============================================
   按钮系统
   ============================================ */
QPushButton#primaryButton {
    background-color: #6B7FEB;
    color: white;
    border-radius: 12px;
    padding: 10px 16px;
    font-weight: 600;
}

QPushButton#primaryButton:hover {
    background-color: #5A6FE0;
    border: 1px solid #7B8FF5;
}

QPushButton#primaryButton:pressed {
    background-color: #4A5FD0;
}

QPushButton#secondaryButton {
    background-color: rgba(255, 255, 255, 0.05); /* Glassy white */
    color: #E0E0E0;
    border: 1px solid #2D2D44;
    border-radius: 12px;
    padding: 8px 16px;
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
    padding: 8px 16px;
}

QPushButton#dangerButton:hover {
    background-color: rgba(231, 76, 60, 0.25);
    border-color: #FF6B6B;
}

/* ============================================
   表格与列表
   ============================================ */
QTableWidget {
    background-color: #242738;
    border: 1px solid #2D2F44;
    border-radius: 12px;  /* 减小圆角避免裁剪内容 */
    gridline-color: #2D2F44;
    color: #E0E4F0;
    selection-background-color: rgba(107, 127, 235, 0.2);
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
    background-color: #6B7FEB;
    border-radius: 6px;
}

QComboBox {
    background-color: #151520;
    border: 1px solid #2D2D44;
    border-radius: 12px;
    padding: 8px 12px;
    color: #FFFFFF;
    combobox-popup: 0; /* Force custom styling on macOS */
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #6B7FEB;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #242738;
    border: 1px solid #2D2F44;
    border-radius: 12px;
    padding: 4px;
    outline: none;
    selection-background-color: transparent;
}

QComboBox QAbstractItemView::item {
    color: #E0E4F0;
    padding: 8px 12px;
    min-height: 24px;
    border-radius: 8px; /* Rounded selection */
    margin: 2px 0;
}

QComboBox QAbstractItemView::item:selected {
    background-color: #6B7FEB;
    color: #FFFFFF;
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
