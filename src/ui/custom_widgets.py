from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt

class PremiumSpinBox(QWidget):
    valueChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        from PyQt6.QtWidgets import QSizePolicy
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed) # Prevent auto-expansion
        self._value = 0
        self._min = 0
        self._max = 9999999 # Effectively no limit by default
        self._step = 1
        self._suffix = ""

        self.init_ui()

    def init_ui(self):
        from PyQt6.QtGui import QIntValidator
        from PyQt6.QtWidgets import QLabel, QVBoxLayout

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0) # No gap for capsule look

        # Value Input
        self.display = QLineEdit()
        self.display.setReadOnly(False)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.display.setObjectName("premiumSpinBoxDisplay")
        self.display.setValidator(QIntValidator(self._min, self._max, self))
        
        # Suffix Label
        self.suffix_label = QLabel("")
        self.suffix_label.setObjectName("premiumSpinBoxSuffix")
        
        # Button Container (Vertical)
        btn_layout = QVBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(0) 
        
        # Buttons (Arrows)
        self.btn_plus = QPushButton("+") # Up arrow
        self.btn_plus.setObjectName("premiumSpinBoxBtnPlus")
        self.btn_plus.setFixedSize(28, 20) 
        self.btn_plus.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.btn_minus = QPushButton("-") # Down arrow
        self.btn_minus.setObjectName("premiumSpinBoxBtnMinus")
        self.btn_minus.setFixedSize(28, 20)
        self.btn_minus.setCursor(Qt.CursorShape.PointingHandCursor)

        btn_layout.addWidget(self.btn_plus)
        btn_layout.addWidget(self.btn_minus)

        layout.addWidget(self.display, 1) # Give expansion to input
        layout.addWidget(self.suffix_label)
        layout.addLayout(btn_layout)

        # Connect signals
        self.btn_plus.clicked.connect(self.increment) 
        self.btn_minus.clicked.connect(self.decrement)
        self.display.editingFinished.connect(self._on_editing_finished)

    def _on_editing_finished(self):
        try:
            val = int(self.display.text())
            self.setValue(val)
        except ValueError:
            self._update_display() # Reset on invalid

    def _update_display(self):
        self.display.setText(str(self._value))
        self.suffix_label.setText(self._suffix)

    def value(self):
        return self._value

    def setValue(self, val):
        val = max(self._min, min(self._max, val))
        if val != self._value:
            self._value = val
            self._update_display()
            self.valueChanged.emit(self._value)

    def setRange(self, min_val, max_val):
        self._min = min_val
        self._max = max_val
        self.setValue(self._value)

    def setSuffix(self, suffix):
        self._suffix = suffix
        self._update_display()

    def setSingleStep(self, step):
        self._step = step

    def increment(self):
        self._sync_text_to_value()
        self.setValue(self._value + self._step)

    def decrement(self):
        self._sync_text_to_value()
        self.setValue(self._value - self._step)
        
    def _sync_text_to_value(self):
        try:
            current_text_val = int(self.display.text())
            # Don"t use setValue here to avoid recursive updates or double signals, 
            # just update internal state to base calculation on what user sees.
            self._value = current_text_val
        except ValueError:
            pass # Keep internal value if text is invalid

    def setMinimumWidth(self, width):
        super().setMinimumWidth(width)
        # Calculate space for buttons (28px) and suffix (approx width or just let it shrink)
        # We need to enforce Fixed width on the line edit to stop it from expanding
        # Suffix width is variable, but buttons are fixed 28.
        # Let's set a small fixed width on display if total width is small.
        
        # ACTUALLY: The user wants to CONTROL the width. 
        # So we should pass this width constraint down.
        # But since we have a layout, setting min width on the container *should* work if children are not expanding.
        # The issue is QLineEdit expands by default.
        self.display.setMinimumWidth(0)
        self.setFixedWidth(width) # FORCE fixed width on the container 

