from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import pyqtgraph as pg


class LineGraph:
    def __init__(self, parent, geometry, minimum_size, maximum_size,
                 styles, labels, colors, variables, group_box_style,
                 background_color, grids, texts, add_legends=False):

        self.variables = variables
        x, y, width, height = geometry
        self.texts = texts
        self.TextObjects = {}
        self.data_lines = {}
        self.group_box = QGroupBox(parent)
        self.group_box.setGeometry(QRect(x, y, width, height))
        self.group_box.setMinimumSize(minimum_size)
        self.group_box.setMaximumSize(maximum_size)
        self.group_box.setStyleSheet(group_box_style)
        self.group_box.show()
        self.graph = pg.PlotWidget(self.group_box)
        self.graph.setGeometry(10, 10, width - 20, height - 20)
        self.graph.setBackground(background_color)
        self.graph.showGrid(x=grids["x"], y=grids["y"])
        if add_legends: self.graph.addLegend()
        self.setup_labels(labels, styles)
        self.setup_graph(self.variables)
        self.setup_texts(texts)
        self.graph.show()
        # self.plots[key].setData(self.time, self.variables[key])

    def setup_labels(self, labels, styles):
        for key in labels:
            position, text, unit = labels[key]["position"], labels[key]["text"], labels[key]["unit"]
            self.graph.setLabel(position, text, units=unit, **styles)

    def limit_time_interval(self, data_length):
        if data_length == 0:
            time_interval = [-2, -1]
        else:
            time_interval = list(range(data_length - min(11, data_length), data_length))[0: data_length]
        return time_interval

    def limit_data(self, data, data_length):
        if data_length == 0:
            # If the data_length is 0, then set data = [0, 0] to avoid any errors.
            # There need to be a time 
            data = [0, 0]
        elif data_length == 11:
            data = data
        elif data_length < 11:
            data = data[0: 12]
        else:
            data = data[(data_length - 1) - 11: data_length - 1]
            # If the data_length is lower than 11, the line above will return the entire list.
            # Otherwise, it will return the last 11 elements in the list.
        return data

    def setup_graph(self, variables):
        for key in variables:
            name, value = key, variables[key]["values"]
            pen = pg.mkPen(color=variables[key]["pen"]["color"], width=variables[key]["pen"]["width"])
            self.data_lines[key] = self.graph.plot(pen=pen,
                                                   name=name,
                                                   symbol=variables[key]["symbol"]["key"],
                                                   symbolSize=variables[key]["symbol"]["size"],
                                                   symbolBrush=variables[key]["symbol"]["color"])
        self.graph.setXRange(0.5, 10.5, padding=0)
        self.graph.setYRange(-50, 50, padding=0)
        # self.graph.setYRange(initial_value, final_value, padding=padding)

    def update_graph(self):
        for key in self.variables:
            data = self.variables[key]['values']
            data_length = len(data)
            time_interval = self.limit_time_interval(data_length)
            if len(time_interval) > 1:
                self.graph.setXRange(time_interval[1] - 0.5, time_interval[1] + 9.5, padding=0)
            else:
                self.graph.setXRange(0.5, 10.5, padding=0)
            data = self.limit_data(data, data_length)
            self.update_text(key, data[-1])
            self.data_lines[key].setData(x=time_interval, y=data)

    def append_to_data(self, dictionary):
        for key in dictionary:
            self.variables[key]['values'].append(dictionary[key])

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
