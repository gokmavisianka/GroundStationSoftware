from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class ConditionLabel:
    def __init__(self, base_text, geometry, minimum_size, maximum_size,
                 data, font, parent, initial_value, border):
        self.font_property = font
        self.font = QFont()
        self.font.setPointSize(font["size"])
        x, y, width, height = geometry
        self.base_text = base_text
        self.border_colors = data["border_color"]
        self.colors = data["colors"]
        self.texts = data["texts"]
        self.condition = initial_value
        self.label = QLabel(parent)
        self.border = border
        self.label.setGeometry(QRect(x, y, width, height))
        self.label.setMinimumSize(minimum_size)
        self.label.setMaximumSize(maximum_size)
        self.label.setFont(self.font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.show()
        self.set_condition(initial_value)

    def set_condition(self, value):
        self.label.setStyleSheet \
            (f"color: {self.font_property['color']}; background-color: {self.colors[value]}; border: {self.border['width']}px solid {self.border_colors[value]};")
        self.label.setText(f"{self.base_text}: {self.texts[value]}")
        self.condition = value
