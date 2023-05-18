from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import pyqtgraph as pg
from random import randint


class BarGraph:
    def __init__(self, name, geometry, width, brush, variables,
                 minimum_size, maximum_size, group_box_style,
                 styles, parent, labels, colors, grids, texts,
                 add_legends=True, background_color="black"):

        x, y, width, height = geometry
        self.items = {}
        self.texts = texts
        self.TextObjects = {}
        self.styles = styles
        self.group_box = QGroupBox(parent)
        self.group_box.setMinimumSize(minimum_size)
        self.group_box.setMaximumSize(maximum_size)
        self.group_box.setGeometry(QRect(x, y, width, height))
        self.group_box.setStyleSheet(group_box_style)
        self.group_box.show()
        self.graph = pg.PlotWidget(self.group_box)
        self.graph.setGeometry(10, 10, width - 20, height - 20)
        self.graph.setBackground(background_color)
        self.graph.showGrid(y=grids["y"])
        self.graph.setYRange(-50, 50, padding=0)
        if add_legends:  self.graph.addLegend(offset=(15, 48))
        self.setup_labels(labels)
        self.setup_texts(texts)
        self.setup_bar_graph_items(variables, colors)
        self.graph.show()

    def setup_labels(self, labels):
        for key in labels:
            position, text, unit = labels[key]["position"], labels[key]["text"], labels[key]["unit"]
            self.graph.setLabel(position, text, units=unit, **self.styles)

    def setup_bar_graph_items(self, variables, colors):
        for i in range(3):
            key, value = list(variables.items())[i]
            self.items[key] = pg.BarGraphItem(name=key, width=0.5, brush=colors[i], x=[i + 1], y1=value)
            self.graph.addItem(self.items[key])

    def update_bar_graph_items(self, variables, colors=["red", "green", "blue"]):
        for i in range(3):
            key, value = list(variables.items())[i]
            self.items[key].setOpts(x=[i + 1], y1=value)
            self.update_text(key, value)
            # If the latency is not important, then this can be done as follows too:
            # self.graph.removeItem(self.items[key])
            # self.items[key] = pg.BarGraphItem(name=key, width=0.5, brush=colors[i], x=[i + 1], y1=item)
            # self.graph.addItem(self.items[key])
        self.variables = variables
            
    def setup_texts(self, texts):
        for key in texts:
            text = QLabel(self.group_box)
            value = f"{texts[key]['value']}: ???"
            text.setText(value)
            x, y, width, height = texts[key]["geometry"]
            text.setGeometry(QRect(x, y, width, height))
            font = QFont()
            font.setPointSize(texts[key]["font"]["size"])
            text.setFont(font)
            text.setStyleSheet(f"color: {texts[key]['font']['color']}")
            text.show()
            self.TextObjects[key] = text

    def update_text(self, key, value):
        self.TextObjects[key].setText(f"{self.texts[key]['value']}: {value}")
        
