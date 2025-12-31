"""
Dashboard 统计卡片组件
显示发送统计、成功率等
"""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt


class StatsCard(QFrame):
    """统计卡片"""
    
    def __init__(self, title: str, value: str, icon: str = "📊", card_type: str = "info"):
        super().__init__()
        
        # 设置卡片类型
        if card_type == "success":
            self.setObjectName("statsCardSuccess")
        elif card_type == "warning":
            self.setObjectName("statsCardWarning")
        elif card_type == "info":
            self.setObjectName("statsCardInfo")
        else:
            self.setObjectName("statsCard")
        
        self.setFixedHeight(120)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        # 图标和标题
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        header_layout.addWidget(icon_label)
        
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # 数值
        value_label = QLabel(value)
        value_label.setObjectName("statValue")
        value_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(value_label)
        
        # 标题
        title_label = QLabel(title)
        title_label.setObjectName("statLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(title_label)
        
        layout.addStretch()
    
    def update_value(self, value: str):
        """更新数值"""
        for child in self.findChildren(QLabel):
            if child.objectName() == "statValue":
                child.setText(value)
                break


class Dashboard(QWidget):
    """Dashboard 面板"""
    
    def __init__(self):
        super().__init__()
        
        layout = QHBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 16)
        
        # 创建4个统计卡片
        self.total_card = StatsCard("总发送邮件", "0", "📧", "info")
        self.success_card = StatsCard("成功率", "0%", "✅", "success")
        self.today_card = StatsCard("今日发送", "0", "📅", "warning")
        self.contacts_card = StatsCard("联系人总数", "0", "👥", "card")
        
        layout.addWidget(self.total_card)
        layout.addWidget(self.success_card)
        layout.addWidget(self.today_card)
        layout.addWidget(self.contacts_card)
    
    def update_stats(self, total: int = 0, success_rate: float = 0, 
                     today: int = 0, contacts: int = 0):
        """更新统计数据"""
        self.total_card.update_value(str(total))
        self.success_card.update_value(f"{success_rate:.1f}%")
        self.today_card.update_value(str(today))
        self.contacts_card.update_value(str(contacts))
