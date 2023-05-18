from PySide2.QtWidgets import *
from datetime import datetime
from PySide2.QtCore import *
from PySide2.QtGui import *
import serial
import serial.tools.list_ports
from random import randint
import pandas as pd

names = ("temperature", "pressure", "altitude")
ports = ("COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "COM10")
baudrates = ["1200", "2400", "4800", "9600", "14400", "19200", "28800", "38400", "57600", "115200", "230400"]


class SerialPort:
    def __init__(self, geometry, parent, font, background_color, border, ConditionLabels, LineGraphs, BarGraphs, V3Ds):
        self.ConditionLabels = ConditionLabels
        self.LineGraphs = LineGraphs
        self.BarGraphs = BarGraphs
        self.V3Ds = V3Ds
        self.data_loader = self.DataLoader(ConditionLabels, LineGraphs, BarGraphs, V3Ds)
        self.combo_boxes = {}
        self.buttons = {}
        self.labels = {}
        self.simulate = True
        self.port = "COM8"
        self.baudrate = 9600
        x, y, width, height = geometry
        self.bridge = None
        self.outputs = []
        self.to_write = []
        self.available_ports = []
        self.font = QFont()
        self.font.setPointSize(font["size"])
        self.group_box = QGroupBox(parent)
        self.group_box.setGeometry(QRect(x, y, width, height))
        self.group_box.show()
        # self.group_box.setStyleSheet(group_box_style)
        self.connected = False

        self.labels["condition"] = None
        self.labels["output"] = None

        self.setup_labels(font, background_color, border)
        self.setup_push_buttons()
        self.setup_combo_boxes()        

    def setup_labels(self, font_property, background_color, border):
        self.labels["output"] = QLabel(self.group_box)
        self.labels["output"].setGeometry(QRect(10, 10, 800, 510))
        self.labels["output"].setStyleSheet(f"color: {font_property['color']}; background-color: {background_color}; border: {border['width']}px solid {border['color']};")
        self.labels["output"].setFont(self.font)
        self.labels["output"].setAlignment(Qt.AlignBottom | Qt.AlignLeft)
        self.labels["output"].show()

    def setup_push_buttons(self):
        width, height, y = 250, 60, 520
        
        def setup_connect_button():
            button = QPushButton("Bağlantı Kur", self.group_box)
            button.setGeometry(QRect(285, y + 10, width, height))
            button.setStyleSheet("background-color:rgb(255, 140, 0);")
            button.setFont(self.font)
            button.clicked.connect(self.connect)
            button.setDisabled(False)
            button.show()
            
            self.buttons["connect"] = button

        def setup_disconnect_button():
            button = QPushButton("Bağlantıyı Kopar", self.group_box)
            button.setGeometry(QRect(285, y + 80, width, height))
            button.setStyleSheet("background-color:rgb(255, 140, 0);")
            button.setFont(self.font)
            button.clicked.connect(self.disconnect)
            button.setDisabled(False)
            button.show()

            self.buttons["disconnect"] = button

        def setup_clear_button():
            button = QPushButton("Temizle", self.group_box)
            button.setGeometry(QRect(560, y + 10, width, height))
            button.setStyleSheet("background-color:rgb(255, 140, 0);")
            button.setFont(self.font)
            button.clicked.connect(self.clear)
            button.setDisabled(False)
            button.show()

            self.buttons["clear"] = button

        setup_connect_button()
        setup_disconnect_button()
        setup_clear_button()

    def setup_combo_boxes(self):
        width, height, y = 250, 60, 520
        
        def setup_ports_combo_box():
            combo_box = QComboBox(self.group_box)
            combo_box.setGeometry(QRect(10, y + 10, width, height))
            combo_box.setStyleSheet("background-color:rgb(255, 140, 0); border: 2px solid rgb(170, 80, 0);")
            combo_box.setFont(self.font)
            combo_box.addItem("Port Seçilmedi")
            combo_box.show()

            self.combo_boxes["ports"] = combo_box

        def setup_baudrates_combo_box():
            combo_box = QComboBox(self.group_box)
            combo_box.setGeometry(QRect(10, y + 80, width, height))
            combo_box.setStyleSheet("background-color:rgb(255, 140, 0); border: 2px solid rgb(170, 80, 0);")
            combo_box.setFont(self.font)
            combo_box.addItem("Baudrate Seçilmedi")
            combo_box.addItems(baudrates)
            combo_box.show()

            self.combo_boxes["baudrates"] = combo_box

        setup_ports_combo_box()
        setup_baudrates_combo_box()

    def get_available_ports(self):
        self.available_ports = ["Port Seçilmedi"] + [comport.device for comport in serial.tools.list_ports.comports()]
        if self.combo_boxes["ports"].currentText() == "":
            self.combo_boxes["ports"].setCurrentIndex(0)
        self.update_available_ports(new_items=self.available_ports)
        self.combo_boxes["ports"].update()

    def update_available_ports(self, new_items):
        old_items = [self.combo_boxes["ports"].itemText(i) for i in range(self.combo_boxes["ports"].count())]
        for old_item, new_item in zip(old_items, new_items):
            if new_item not in old_items:
                self.combo_boxes["ports"].addItem(new_item)
            if old_item not in new_items:
                self.combo_boxes["ports"].removeItem(old_items.index(old_item))
        self.combo_boxes["ports"].update()

    def connect(self):
        port = self.combo_boxes["ports"].currentText()
        baudrate = self.combo_boxes["baudrates"].currentText()
        if port in ports and baudrate in baudrates:
            try:
                try:
                    self.bridge.close()
                except AttributeError:
                    pass
                self.bridge = serial.Serial(port=port, baudrate=int(baudrate), timeout=0.1)
                self.labels["condition"].set_condition(True)
                self.outputs.append("- Bağlantı başarıyla kuruldu!")
            except serial.serialutil.SerialException:
                self.outputs.append("- Bağlantı kurulamadı, Port meşgul.")
        else:
            self.outputs.append("- Port veya Baudrate değeri hatalı!")

    def disconnect(self):
        try:
            self.bridge.close()
            self.outputs.append("- Bağlantı başarıyla koparıldı.")
        except AttributeError:
            pass
        self.bridge = None
        self.labels["condition"].set_condition(False)

    def show_outputs(self, limit=20):
        self.outputs = self.outputs[-limit:]
        self.labels["output"].setText("\n".join(output for output in self.outputs))

    def clear(self):
        self.outputs = ["- Tüm satırlar temizlendi."]
        self.project()

    def project(self):
        h, m, s = self.get_time()
        data = self.get_data()
        self.to_write.append(data)
        if len(self.to_write) == 0:
            self.outputs.append(f"{h:02}:{m:02}:{s:02} >>> ")
        else:
            self.to_write.remove("")
            for data in self.to_write:
                self.outputs.append(f"{h:02}:{m:02}:{s:02} >>> {data}")
        self.show_outputs()
        self.to_write.clear()

    def get_time(self):
        time = datetime.now()
        return time.hour, time.minute, time.second

    def get_data(self):
        data = b""
        try:
            data = self.bridge.readlines()[-1].strip(b"\r\n")
            return str(data, "utf-8")
        except AttributeError:
            self.get_available_ports()
        except serial.serialutil.SerialException:
            self.bridge = None
            self.labels["condition"].set_condition(False)
            self.get_available_ports()
        except IndexError:
            pass
        finally:
            return ""

    @staticmethod
    def random_data(length=6):
        return ":".join(str(randint(0, 100)) for number in range(length))

    class DataLoader:
        def __init__(self, ConditionLabels, LineGraphs, BarGraphs, V3Ds):
            self.ConditionLabels = ConditionLabels
            self.LineGraphs = LineGraphs
            self.BarGraphs = BarGraphs
            self.V3Ds = V3Ds
            self.time_data = [self.get_time()]
            self.dictionary = {"rocket" : {"temperature": [0.0], "pressure": [0.0], "altitude": [0.0]},
                               "payload": {"temperature": [0.0], "pressure": [0.0], "altitude": [0.0]}}
            self.data_frame = pd.DataFrame(data=self.dictionary)

        def update(self, sub_dictionary):
            self.time_data.append(self.get_time())
            for key1 in sub_dictionary:
                for key2 in sub_dictionary[key1]:
                    self.dictionary[key1][key2].append(sub_dictionary[key1][key2])
                    self.LineGraphs[key2].variables[key1]["value"] = self.dictionary[key1][key2]
                    self.LineGraphs[key2].draw()

        def define(self, LineGraphs):
            self.LineGraphs = LineGraphs

        @staticmethod
        def get_time() -> str:
            time = datetime.now()
            return f"{time.hour:02}:{time.minute:02}:{time.second:02}"

        @staticmethod
        def is_float(string):
            try:
                float(string)
                return True
            except ValueError:
                return False

        def pump(self, output: list):
            length = len(output)
            sub_dictionary = {"rocket": {}, "payload": {}}
            for index in range(length):
                key1 = "rocket" if index < 3 else "payload"
                key2 = names[index % 3]
                value = output[index]
                condition = self.is_float(value)
                if condition is False:
                    if len(self.dictionary[key1][key2]) != 0:
                        value = sum(self.dictionary[key1][key2]) / len(self.dictionary[key1][key2])
                    else:
                        value = 0.0
                else:
                    value = float(value)
                sub_dictionary[key1][key2] = value
            self.update(sub_dictionary)

        def filter(self, input: str, target_length=6):
            output = input.split(":")
            length = len(output)
            if length == target_length:
                self.pump(output)
            elif length < target_length:
                difference = target_length - length
                for number in range(difference):
                    input += ":"
                self.filter(input)
            else:
                input = ":".join(output[:target_length])
                self.filter(input)
