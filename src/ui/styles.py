"""
macOS 风格样式表
支持系统深色模式
"""

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
