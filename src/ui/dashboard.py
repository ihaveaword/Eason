"""
Dashboard 统计卡片组件 - 极简风格
"""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt


class StatsCard(QFrame):
    """统计卡片 - 极简设计"""
    
    def __init__(self, title: str, value: str, icon: str = "📊", card_type: str = "info"):
        super().__init__()
        
        # 统一样式，不再区分类型
        self.setObjectName("statsCard")
        self.setMinimumHeight(110)
        self.setMinimumWidth(140)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # 标题
        title_label = QLabel(title)
        title_label.setObjectName("statLabel")
        title_label.setWordWrap(False)
        layout.addWidget(title_label)
        
        layout.addSpacing(4)
        
        # 数值
        value_label = QLabel(value)
        value_label.setObjectName("statValue")
        value_label.setWordWrap(False)
        layout.addWidget(value_label)
        
        layout.addStretch()
    
    def update_value(self, value: str):
        """更新数值"""
        for child in self.findChildren(QLabel):
            if child.objectName() == "statValue":
                child.setText(value)
                break


class Dashboard(QWidget):
    """Dashboard 面板 - 极简风格"""
    
    def __init__(self):
        super().__init__()
        
        layout = QHBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 8, 0, 20)
        
        # 创建4个统计卡片
        self.total_card = StatsCard("总发送", "0")
        self.success_card = StatsCard("成功率", "0%")
        self.today_card = StatsCard("今日", "0")
        self.contacts_card = StatsCard("联系人", "0")
        
        layout.addWidget(self.total_card)
        layout.addWidget(self.success_card)
        layout.addWidget(self.today_card)
        layout.addWidget(self.contacts_card)
    
    def update_stats(self, total: int = 0, success_rate: float = 0, 
                     today: int = 0, contacts: int = 0):
        """更新统计数据"""
        self.total_card.update_value(str(total))
        self.success_card.update_value(f"{success_rate:.0f}%")
        self.today_card.update_value(str(today))
        self.contacts_card.update_value(str(contacts))
