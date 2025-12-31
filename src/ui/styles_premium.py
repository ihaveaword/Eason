"""
商业级样式系统 - 亮色主题
包含卡片、阴影、渐变、动效
"""

LIGHT_THEME_PREMIUM = """
/* ============================================
   全局样式
   ============================================ */
QMainWindow {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 #f8f9fa, stop:1 #e9ecef
    );
}

/* ============================================
   卡片样式
   ============================================ */
QGroupBox {
    font-weight: 600;
    font-size: 14px;
    border: none;
    border-radius: 12px;
    margin-top: 12px;
    padding: 20px;
    background-color: white;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 16px;
    padding: 0 8px;
    color: #2c3e50;
    font-size: 15px;
}

/* ============================================
   统计卡片（特殊样式）
   ============================================ */
QFrame[objectName="statsCard"] {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #667eea, stop:1 #764ba2
    );
    border-radius: 16px;
    padding: 24px;
}

QFrame[objectName="statsCardSuccess"] {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #56ab2f, stop:1 #a8e063
    );
    border-radius: 16px;
    padding: 24px;
}

QFrame[objectName="statsCardInfo"] {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #2193b0, stop:1 #6dd5ed
    );
    border-radius: 16px;
    padding: 24px;
}

QFrame[objectName="statsCardWarning"] {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #f7971e, stop:1 #ffd200
    );
    border-radius: 16px;
    padding: 24px;
}

/* ============================================
   按钮系统
   ============================================ */
QPushButton {
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #667eea, stop:1 #764ba2
    );
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 14px;
    min-height: 36px;
}

QPushButton:hover {
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #7b8cff, stop:1 #8a5fb8
    );
}

QPushButton:pressed {
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #5567d8, stop:1 #653a8e
    );
    padding-top: 12px;
}

QPushButton:disabled {
    background: #e0e0e0;
    color: #9e9e9e;
}

/* 成功按钮 */
QPushButton#successButton {
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #56ab2f, stop:1 #a8e063
    );
}

QPushButton#successButton:hover {
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #6bc043, stop:1 #bef577
    );
}

/* 停止按钮 */
QPushButton#stopButton {
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #eb3349, stop:1 #f45c43
    );
}

QPushButton#stopButton:hover {
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #ff4757, stop:1 #ff6b5d
    );
}

/* 次要按钮 */
QPushButton#secondaryButton {
    background: white;
    color: #667eea;
    border: 2px solid #667eea;
}

QPushButton#secondaryButton:hover {
    background: #f0f2ff;
}

/* 主题切换按钮 */
QPushButton#themeButton {
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #5e5ce6, stop:1 #9f7aea
    );
    min-width: 120px;
    border-radius: 20px;
    padding: 8px 16px;
}

QPushButton#themeButton:hover {
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #7d7aff, stop:1 #b794f6
    );
}

/* ============================================
   输入框样式
   ============================================ */
QLineEdit, QTextEdit, QSpinBox {
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    padding: 10px 14px;
    background-color: white;
    color: #2c3e50;
    font-size: 14px;
    selection-background-color: #667eea;
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus {
    border: 2px solid #667eea;
    background-color: #f8f9ff;
}

QLineEdit:hover, QTextEdit:hover, QSpinBox:hover {
    border-color: #b0b0b0;
}

/* ============================================
   下拉框样式
   ============================================ */
QComboBox {
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    padding: 8px 14px;
    background-color: white;
    color: #2c3e50;
    font-size: 14px;
    min-height: 36px;
}

QComboBox:hover {
    border-color: #b0b0b0;
}

QComboBox:focus {
    border: 2px solid #667eea;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #667eea;
    margin-right: 8px;
}

QComboBox QAbstractItemView {
    background-color: white;
    border: 2px solid #667eea;
    border-radius: 8px;
    selection-background-color: #667eea;
    selection-color: white;
    padding: 4px;
}

/* ============================================
   进度条样式
   ============================================ */
QProgressBar {
    border: none;
    border-radius: 10px;
    text-align: center;
    background-color: #f0f0f0;
    color: #2c3e50;
    height: 28px;
    font-weight: 600;
    font-size: 13px;
}

QProgressBar::chunk {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb
    );
    border-radius: 10px;
}

/* ============================================
   标签样式
   ============================================ */
QLabel {
    color: #2c3e50;
    font-size: 14px;
}

QLabel[objectName="statValue"] {
    color: white;
    font-size: 32px;
    font-weight: 700;
}

QLabel[objectName="statLabel"] {
    color: rgba(255, 255, 255, 0.9);
    font-size: 14px;
    font-weight: 500;
}

/* ============================================
   标签页样式
   ============================================ */
QTabWidget::pane {
    border: none;
    border-radius: 12px;
    background-color: white;
    padding: 16px;
}

QTabBar::tab {
    background-color: #f5f5f5;
    color: #666;
    padding: 12px 24px;
    margin-right: 4px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    font-size: 14px;
    font-weight: 500;
}

QTabBar::tab:selected {
    background-color: white;
    color: #667eea;
    font-weight: 600;
}

QTabBar::tab:hover:!selected {
    background-color: #e8e8e8;
    color: #444;
}

/* ============================================
   复选框样式
   ============================================ */
QCheckBox {
    color: #2c3e50;
    font-size: 14px;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border: 2px solid #e0e0e0;
    border-radius: 4px;
    background-color: white;
}

QCheckBox::indicator:hover {
    border-color: #667eea;
}

QCheckBox::indicator:checked {
    background-color: #667eea;
    border-color: #667eea;
    image: url(none);
}

/* ============================================
   滚动条样式
   ============================================ */
QScrollBar:vertical {
    background: #f5f5f5;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background: #c0c0c0;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #a0a0a0;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""

# 暗色主题 - 商业级
DARK_THEME_PREMIUM = """
/* ============================================
   全局样式 - 暗色
   ============================================ */
QMainWindow {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 #1a1a2e, stop:1 #16213e
    );
}

QGroupBox {
    font-weight: 600;
    font-size: 14px;
    border: none;
    border-radius: 12px;
    margin-top: 12px;
    padding: 20px;
    background-color: #0f3460;
    color: #e9ecef;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 16px;
    padding: 0 8px;
    color: #e9ecef;
    font-size: 15px;
}

QFrame[objectName="statsCard"] {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #667eea, stop:1 #764ba2
    );
    border-radius: 16px;
    padding: 24px;
}

QFrame[objectName="statsCardSuccess"] {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #56ab2f, stop:1 #a8e063
    );
    border-radius: 16px;
    padding: 24px;
}

QFrame[objectName="statsCardInfo"] {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #2193b0, stop:1 #6dd5ed
    );
    border-radius: 16px;
    padding: 24px;
}

QFrame[objectName="statsCardWarning"] {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #f7971e, stop:1 #ffd200
    );
    border-radius: 16px;
    padding: 24px;
}

QPushButton {
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #667eea, stop:1 #764ba2
    );
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 14px;
    min-height: 36px;
}

QPushButton:hover {
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #7b8cff, stop:1 #8a5fb8
    );
}

QPushButton:pressed {
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #5567d8, stop:1 #653a8e
    );
}

QPushButton#successButton {
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #56ab2f, stop:1 #a8e063
    );
}

QPushButton#stopButton {
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #eb3349, stop:1 #f45c43
    );
}

QPushButton#secondaryButton {
    background: #0f3460;
    color: #e9ecef;
    border: 2px solid #667eea;
}

QPushButton#secondaryButton:hover {
    background: #16213e;
}

QPushButton#themeButton {
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #5e5ce6, stop:1 #9f7aea
    );
    min-width: 120px;
    border-radius: 20px;
}

QLineEdit, QTextEdit, QSpinBox {
    border: 2px solid #16213e;
    border-radius: 8px;
    padding: 10px 14px;
    background-color: #0f3460;
    color: #e9ecef;
    font-size: 14px;
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus {
    border: 2px solid #667eea;
    background-color: #16213e;
}

QComboBox {
    border: 2px solid #16213e;
    border-radius: 8px;
    padding: 8px 14px;
    background-color: #0f3460;
    color: #e9ecef;
    font-size: 14px;
}

QComboBox:focus {
    border: 2px solid #667eea;
}

QComboBox QAbstractItemView {
    background-color: #0f3460;
    border: 2px solid #667eea;
    color: #e9ecef;
    selection-background-color: #667eea;
}

QProgressBar {
    border: none;
    border-radius: 10px;
    background-color: #16213e;
    color: #e9ecef;
    height: 28px;
    font-weight: 600;
}

QProgressBar::chunk {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #667eea, stop:1 #f093fb
    );
    border-radius: 10px;
}

QLabel {
    color: #e9ecef;
    font-size: 14px;
}

QLabel[objectName="statValue"] {
    color: white;
    font-size: 32px;
    font-weight: 700;
}

QLabel[objectName="statLabel"] {
    color: rgba(255, 255, 255, 0.9);
    font-size: 14px;
}

QTabWidget::pane {
    border: none;
    border-radius: 12px;
    background-color: #0f3460;
    padding: 16px;
}

QTabBar::tab {
    background-color: #16213e;
    color: #adb5bd;
    padding: 12px 24px;
    margin-right: 4px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
}

QTabBar::tab:selected {
    background-color: #0f3460;
    color: #667eea;
    font-weight: 600;
}

QCheckBox {
    color: #e9ecef;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border: 2px solid #16213e;
    border-radius: 4px;
    background-color: #0f3460;
}

QCheckBox::indicator:checked {
    background-color: #667eea;
    border-color: #667eea;
}

QScrollBar:vertical {
    background: #16213e;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background: #667eea;
    border-radius: 5px;
}
"""
