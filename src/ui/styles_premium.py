"""
极简主义样式系统 - Minimalist Design
参考: Vercel, Linear, Arc Browser
方案B: 蓝灰色调轻柔版
"""

LIGHT_THEME_PREMIUM = """
/* ============================================
   全局样式 - 蓝灰色调轻柔版
   ============================================ */
QMainWindow {
    background-color: #F8FAFC;
}

/* ============================================
   卡片样式 - 蓝灰边框
   ============================================ */
QGroupBox {
    font-weight: 500;
    font-size: 13px;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    margin-top: 8px;
    padding: 20px;
    background-color: white;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: #1E293B;
    font-size: 14px;
    font-weight: 600;
}

/* ============================================
   统计卡片 - 纯白卡片
   ============================================ */
QFrame[objectName="statsCard"] {
    background-color: white;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    min-width: 140px;
    min-height: 100px;
}

QFrame[objectName="statsCardSuccess"] {
    background-color: white;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    min-width: 140px;
    min-height: 100px;
}

QFrame[objectName="statsCardInfo"] {
    background-color: white;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    min-width: 140px;
    min-height: 100px;
}

QFrame[objectName="statsCardWarning"] {
    background-color: white;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    min-width: 140px;
    min-height: 100px;
}

/* ============================================
   按钮系统 - 蓝紫强调色
   ============================================ */
QPushButton {
    background-color: #4F46E5;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 18px;
    font-weight: 500;
    font-size: 13px;
    min-height: 32px;
}

QPushButton:hover {
    background-color: #4338CA;
}

QPushButton:pressed {
    background-color: #3730A3;
}

QPushButton:disabled {
    background-color: #F1F5F9;
    color: #94A3B8;
    border: 1px solid #E2E8F0;
}

/* 主要按钮 */
QPushButton#primaryButton {
    background-color: #4F46E5;
    color: white;
}

QPushButton#primaryButton:hover {
    background-color: #4338CA;
}

/* 成功按钮 */
QPushButton#successButton {
    background-color: #059669;
    color: white;
}

QPushButton#successButton:hover {
    background-color: #047857;
}

/* 危险/停止按钮 */
QPushButton#stopButton, QPushButton#dangerButton {
    background-color: #DC2626;
    color: white;
}

QPushButton#stopButton:hover, QPushButton#dangerButton:hover {
    background-color: #B91C1C;
}

/* 次要按钮 */
QPushButton#secondaryButton {
    background-color: white;
    color: #1E293B;
    border: 1px solid #E2E8F0;
}

QPushButton#secondaryButton:hover {
    background-color: #F8FAFC;
    border-color: #CBD5E1;
}

/* 主题切换按钮 */
QPushButton#themeButton {
    background-color: #EEF2FF;
    color: #4F46E5;
    border: 1px solid #C7D2FE;
    min-width: 100px;
    border-radius: 6px;
    padding: 8px 14px;
}

QPushButton#themeButton:hover {
    background-color: #E0E7FF;
    border-color: #A5B4FC;
}

/* ============================================
   输入框样式 - 蓝灰边框
   ============================================ */
QLineEdit, QTextEdit, QSpinBox {
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    padding: 8px 12px;
    background-color: white;
    color: #1E293B;
    font-size: 13px;
    selection-background-color: #4F46E5;
    selection-color: white;
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus {
    border: 2px solid #4F46E5;
    background-color: white;
}

QLineEdit:hover, QTextEdit:hover, QSpinBox:hover {
    border-color: #CBD5E1;
}

QLineEdit::placeholder, QTextEdit::placeholder {
    color: #94A3B8;
}

/* ============================================
   下拉框样式
   ============================================ */
QComboBox {
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    padding: 8px 12px;
    background-color: white;
    color: #1E293B;
    font-size: 13px;
    min-height: 32px;
}

QComboBox:hover {
    border-color: #CBD5E1;
}

QComboBox:focus {
    border: 2px solid #4F46E5;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #64748B;
    margin-right: 6px;
}

QComboBox QAbstractItemView {
    background-color: white;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    selection-background-color: #EEF2FF;
    selection-color: #1E293B;
    padding: 4px;
}

/* ============================================
   进度条样式 - 蓝紫色
   ============================================ */
QProgressBar {
    border: none;
    border-radius: 4px;
    text-align: center;
    background-color: #E2E8F0;
    color: #1E293B;
    height: 24px;
    font-weight: 500;
    font-size: 12px;
}

QProgressBar::chunk {
    background-color: #4F46E5;
    border-radius: 4px;
}

/* ============================================
   标签样式
   ============================================ */
QLabel {
    color: #1E293B;
    font-size: 14px;
    line-height: 1.4;
}

QLabel[objectName="statValue"] {
    color: #1E293B;
    font-size: 32px;
    font-weight: 700;
    letter-spacing: -0.5px;
    padding-top: 4px;
}

QLabel[objectName="statLabel"] {
    color: #64748B;
    font-size: 13px;
    font-weight: 500;
    padding-bottom: 2px;
}

QLabel[objectName="tipLabel"] {
    color: #64748B;
    font-size: 12px;
}

QLabel[objectName="fieldLabel"] {
    color: #475569;
    font-size: 13px;
    font-weight: 500;
}

/* ============================================
   标签页样式
   ============================================ */
QTabWidget::pane {
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    background-color: white;
    padding: 16px;
}

QTabBar::tab {
    background-color: transparent;
    color: #64748B;
    padding: 12px 24px;
    margin-right: 8px;
    border: none;
    border-bottom: 2px solid transparent;
    font-size: 14px;
    font-weight: 500;
    min-width: 80px;
}

QTabBar::tab:selected {
    color: #4F46E5;
    border-bottom: 2px solid #4F46E5;
    font-weight: 600;
}

QTabBar::tab:hover:!selected {
    color: #1E293B;
}

/* ============================================
   复选框样式
   ============================================ */
QCheckBox {
    color: #1E293B;
    font-size: 13px;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid #CBD5E1;
    border-radius: 4px;
    background-color: white;
}

QCheckBox::indicator:hover {
    border-color: #4F46E5;
}

QCheckBox::indicator:checked {
    background-color: #4F46E5;
    border-color: #4F46E5;
}

/* ============================================
   滚动条样式
   ============================================ */
QScrollBar:vertical {
    background: #F8FAFC;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #CBD5E1;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #94A3B8;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background: #F8FAFC;
    height: 8px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background: #CBD5E1;
    border-radius: 4px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background: #94A3B8;
}

/* ============================================
   表格样式
   ============================================ */
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
    border-radius: 12px;
    min-width: 140px;
    min-height: 100px;
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
    font-size: 14px;
    line-height: 1.4;
}

QLabel[objectName="statValue"] {
    color: #fafafa;
    font-size: 32px;
    font-weight: 700;
    padding-top: 4px;
}

QLabel[objectName="statLabel"] {
    color: #737373;
    font-size: 13px;
    font-weight: 500;
    padding-bottom: 2px;
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
    padding: 12px 24px;
    margin-right: 8px;
    border: none;
    border-bottom: 2px solid transparent;
    font-size: 14px;
    font-weight: 500;
    min-width: 80px;
}

QTabBar::tab:selected {
    color: #fafafa;
    border-bottom: 2px solid #fafafa;
    font-weight: 600;
}

QTabBar::tab:hover:!selected {
    color: #a3a3a3;
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
