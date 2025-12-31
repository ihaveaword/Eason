"""
macOS 风格样式表
支持亮色/暗色主题切换
"""

# 亮色主题
LIGHT_THEME = """
QMainWindow {
    background-color: #f5f5f7;
}
QGroupBox {
    font-weight: 600;
    border: 1px solid #d1d1d6;
    border-radius: 8px;
    margin-top: 8px;
    padding-top: 12px;
    background-color: white;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 5px;
    color: #1d1d1f;
}
QPushButton {
    background-color: #007AFF;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
    font-size: 13px;
    min-height: 28px;
}
QPushButton:hover {
    background-color: #0051D5;
}
QPushButton:pressed {
    background-color: #004FC4;
}
QPushButton:disabled {
    background-color: #d1d1d6;
    color: #8e8e93;
}
QPushButton#stopButton {
    background-color: #FF3B30;
}
QPushButton#stopButton:hover {
    background-color: #D70015;
}
QPushButton#secondaryButton {
    background-color: #8e8e93;
}
QPushButton#secondaryButton:hover {
    background-color: #636366;
}
QPushButton#themeButton {
    background-color: #5856d6;
    min-width: 100px;
}
QPushButton#themeButton:hover {
    background-color: #4745b8;
}
QLineEdit, QTextEdit, QSpinBox, QComboBox {
    border: 1px solid #d1d1d6;
    border-radius: 6px;
    padding: 6px 8px;
    background-color: white;
    color: #1d1d1f;
    selection-background-color: #007AFF;
}
QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 2px solid #007AFF;
}
QProgressBar {
    border: 1px solid #d1d1d6;
    border-radius: 6px;
    text-align: center;
    background-color: #f5f5f7;
    color: #1d1d1f;
    height: 22px;
}
QProgressBar::chunk {
    background-color: #34C759;
    border-radius: 5px;
}
QLabel {
    color: #1d1d1f;
}
QTabWidget::pane {
    border: 1px solid #d1d1d6;
    border-radius: 8px;
    background-color: white;
    padding: 8px;
}
QTabBar::tab {
    background-color: #e5e5ea;
    color: #1d1d1f;
    padding: 8px 20px;
    margin-right: 4px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}
QTabBar::tab:selected {
    background-color: white;
    font-weight: 600;
}
QTabBar::tab:hover:!selected {
    background-color: #d1d1d6;
}
QCheckBox {
    color: #1d1d1f;
}
"""

# 暗色主题
DARK_THEME = """
QMainWindow {
    background-color: #1c1c1e;
}
QGroupBox {
    font-weight: 600;
    border: 1px solid #38383a;
    border-radius: 8px;
    margin-top: 8px;
    padding-top: 12px;
    background-color: #2c2c2e;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 5px;
    color: #f5f5f7;
}
QPushButton {
    background-color: #0a84ff;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
    font-size: 13px;
    min-height: 28px;
}
QPushButton:hover {
    background-color: #409cff;
}
QPushButton:pressed {
    background-color: #0077ed;
}
QPushButton:disabled {
    background-color: #38383a;
    color: #8e8e93;
}
QPushButton#stopButton {
    background-color: #ff453a;
}
QPushButton#stopButton:hover {
    background-color: #ff6961;
}
QPushButton#secondaryButton {
    background-color: #636366;
}
QPushButton#secondaryButton:hover {
    background-color: #8e8e93;
}
QPushButton#themeButton {
    background-color: #5e5ce6;
    min-width: 100px;
}
QPushButton#themeButton:hover {
    background-color: #7d7aff;
}
QLineEdit, QTextEdit, QSpinBox, QComboBox {
    border: 1px solid #38383a;
    border-radius: 6px;
    padding: 6px 8px;
    background-color: #2c2c2e;
    color: #f5f5f7;
    selection-background-color: #0a84ff;
}
QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 2px solid #0a84ff;
}
QProgressBar {
    border: 1px solid #38383a;
    border-radius: 6px;
    text-align: center;
    background-color: #1c1c1e;
    color: #f5f5f7;
    height: 22px;
}
QProgressBar::chunk {
    background-color: #30d158;
    border-radius: 5px;
}
QLabel {
    color: #f5f5f7;
}
QTabWidget::pane {
    border: 1px solid #38383a;
    border-radius: 8px;
    background-color: #2c2c2e;
    padding: 8px;
}
QTabBar::tab {
    background-color: #38383a;
    color: #f5f5f7;
    padding: 8px 20px;
    margin-right: 4px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}
QTabBar::tab:selected {
    background-color: #2c2c2e;
    font-weight: 600;
}
QTabBar::tab:hover:!selected {
    background-color: #48484a;
}
QCheckBox {
    color: #f5f5f7;
}
QComboBox::drop-down {
    border: none;
}
QComboBox QAbstractItemView {
    background-color: #2c2c2e;
    color: #f5f5f7;
    selection-background-color: #0a84ff;
}
"""

# 默认样式（兼容旧代码）
STYLESHEET = """
QMainWindow {
    background-color: palette(window);
}
QGroupBox {
    font-weight: 600;
    border: 1px solid palette(mid);
    border-radius: 8px;
    margin-top: 8px;
    padding-top: 12px;
    background-color: palette(base);
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 5px;
    color: palette(text);
}
QPushButton {
    background-color: #007AFF;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
    font-size: 13px;
    min-height: 28px;
}
QPushButton:hover {
    background-color: #0051D5;
}
QPushButton:pressed {
    background-color: #004FC4;
}
QPushButton:disabled {
    background-color: palette(mid);
    color: palette(disabled-text);
}
QPushButton#stopButton {
    background-color: #FF3B30;
}
QPushButton#stopButton:hover {
    background-color: #D70015;
}
QPushButton#secondaryButton {
    background-color: #8e8e93;
}
QPushButton#secondaryButton:hover {
    background-color: #636366;
}
QLineEdit, QTextEdit, QSpinBox, QComboBox {
    border: 1px solid palette(mid);
    border-radius: 6px;
    padding: 6px 8px;
    background-color: palette(base);
    color: palette(text);
    selection-background-color: #007AFF;
}
QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 2px solid #007AFF;
}
QProgressBar {
    border: 1px solid palette(mid);
    border-radius: 6px;
    text-align: center;
    background-color: palette(window);
    color: palette(text);
    height: 22px;
}
QProgressBar::chunk {
    background-color: #34C759;
    border-radius: 5px;
}
QLabel {
    color: palette(text);
}
QTabWidget::pane {
    border: 1px solid palette(mid);
    border-radius: 8px;
    background-color: palette(base);
    padding: 8px;
}
QTabBar::tab {
    background-color: palette(button);
    color: palette(text);
    padding: 8px 20px;
    margin-right: 4px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}
QTabBar::tab:selected {
    background-color: palette(base);
    font-weight: 600;
}
QTabBar::tab:hover:!selected {
    background-color: palette(midlight);
}
"""
