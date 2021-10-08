import sys
import os
import shutil
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import random
import threading
import time
import pygame

digits = list("0123456789")


def evaloc(row, column, width=1, height=1, case=0, ax=0, ay=0, aw=0, ah=0):
    if case == 0: return [row * 26 + (row - 1) * 183 + ax, column * 26 + (column - 1) * 51 + ay, 183 * width + 26 * (width - 1) + aw, 51 * height + 26 * (height - 1) + ah]
    elif case == 1: return [(row - 1) * (183 + 26) + ax, (column - 1) * (51 + 26) + ay, 183 * width + 26 * (width - 1) + aw, 51 * height + 26 * (height - 1) + ah]
    elif case == 2: return [(row - 1) * (183 + 26) + ax, column * 26 + (column - 1) * 51 + ay, 183 * width + 26 * (width - 1) + aw, 51 * height + 26 * (height - 1) + ah]
    elif case == 3: return [row * 26 + (row - 1) * 183 + ax, (column - 1) * (51 + 26) + ay, 183 * width + 26 * (width - 1) + aw, 51 * height + 26 * (height - 1) + ah]


# noinspection SpellCheckingInspection
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atınç Roket Takımı Yer İstasyonu Yazılımı")
        self.setStyleSheet("background-color:rgb(70,105,145);")
        self.stopThreads = False
        self.setupUi()
        self.show()

    def setupUi(self):
        self.setFixedSize(1280, 720)
        self.setup_Dictionaries_and_Lists()
        self.setup_Tabs()
        self.setup_GroupBoxes()
        self.setup_Templates()
        self.setup_ComboBoxes()
        self.setup_CheckBoxes()
        self.setup_PushButtons()
        self.setup_LineEdits()
        self.setup_Labels()

    def setup_Dictionaries_and_Lists(self):
        self.Tabs = {}
        self.GroupBoxes = {}
        self.templates = {}
        self.TemplateItems = {}
        self.PartItems = {}
        self.ComboBoxes = {}
        self.ComboBoxItems = {}
        self.CheckBoxes = {}
        self.PushButtons = {}
        self.LineEdits = {}
        self.Labels = {}

    def create_font(self, font_size=8):
        local_font = QFont()
        local_font.setPointSize(font_size)
        return local_font

    def decideFunction_0(self, GroupBox, Tab):
        if GroupBox is not None: return self.GroupBoxes[GroupBox]
        elif Tab is not None: return self.Tabs[Tab]
        else: return self

    def quit(self):
        self.stopThreads = True
        self.close()
    # ---------------------------------------------------------------------------------------------------------------- #
    def setup_PushButtons(self):
        self.add_PushButtons("CreateNewTemplate", "Yeni Şablon Oluştur", evaloc(1, 1), target=self.create_template)
        self.add_PushButtons("Exit", "Çıkış", evaloc(1, 9), target=self.quit)
        self.add_PushButtons("DeleteTemplate", "Şablonu Sil", evaloc(5, 1, case=1), GroupBox="RDTemplate", target=self.delete_template)
        self.add_PushButtons("DeletePart", "Parçayı Sil", evaloc(2, 1, case=1), GroupBox="RDPart", target=self.delete_part)
        self.add_PushButtons("CreateNewPart", "Yeni Parça Oluştur", evaloc(1, 1, case=1), GroupBox="RDTemplate", target=self.create_part)
        self.add_PushButtons("Redo", "Geri Al", evaloc(1, 1, case=1), GroupBox="RightBottomButtons", target=self.on_clicked_redo_button)
        self.add_PushButtons("Save", "Kaydet", evaloc(2, 1, case=1), GroupBox="RightBottomButtons", target=self.on_clicked_save_button)
        self.add_PushButtons("Run", "Çalıştır", evaloc(6, 9), visible=False, target=self.on_clicked_run_button)

    def add_PushButtons(self, object_name, object_text, geometry, GroupBox=None, Tab=None, visible=True, font_size=12, target=None):
        x, y, width, height = geometry
        if object_name not in self.PushButtons:
            parent = self.decideFunction_0(GroupBox, Tab)
            self.PushButtons.update({object_name: QPushButton(object_text, self if GroupBox is None else self.GroupBoxes[GroupBox])})
            self.PushButtons[object_name].setGeometry(QRect(x, y, width, height))
            self.PushButtons[object_name].setFont(self.create_font(font_size=font_size))
            self.PushButtons[object_name].setStyleSheet("background-color:rgb(243, 91, 104);")
            self.PushButtons[object_name].show() if visible else self.PushButtons[object_name].hide()
            if target is not None: self.PushButtons[object_name].clicked.connect(target)

    # ---------------------------------------------------------------------------------------------------------------- #
    def setup_CheckBoxes(self):
        # self.add_CheckBox("TestMode", "Test Modu", evaloc(3, 9))
        pass

    def add_CheckBox(self, object_name, object_text, geometry, GroupBox=None, Tab=None, visible=True, layout_direction="RL", borderless=True, font_size=10, target=None):
        x, y, width, height = geometry
        if object_name not in self.CheckBoxes:
            parent = self.decideFunction_0(GroupBox, Tab)
            self.CheckBoxes.update({object_name: QCheckBox(object_text, parent)})
            self.CheckBoxes[object_name].setGeometry(QRect(x, y, width, height))
            self.CheckBoxes[object_name].setFont(self.create_font(font_size=font_size))
            if layout_direction == "RL": self.CheckBoxes[object_name].setLayoutDirection(Qt.RightToLeft)
            else: self.CheckBoxes[object_name].setLayoutDirection(Qt.LeftToRight)
            if visible: self.CheckBoxes[object_name].show()
            else: self.CheckBoxes[object_name].hide()
            if target is not None: self.CheckBoxes[object_name].stateChanged.connect(target)
            if borderless: self.CheckBoxes[object_name].setStyleSheet("border-width:0px;")

    # ---------------------------------------------------------------------------------------------------------------- #
    def setup_ComboBoxes(self):
        pass

    def add_ComboBox(self, object_name, geometry, items, connected_function, GroupBox=None, visible=True, font_size=10,
                     css=True, border_style='solid', border_width='1', border_color='gray', rgb=(175, 220, 220), center=True):
        x, y, width, height = geometry
        if object not in self.ComboBoxes:
            parent = self if GroupBox is None else self.GroupBoxes[GroupBox]
            self.ComboBoxes.update({object_name: QComboBox(parent)})
            self.ComboBoxes[object_name].setGeometry(QRect(x, y, width, height))
            self.ComboBoxes[object_name].currentIndexChanged.connect(connected_function)
            self.ComboBoxes[object_name].setFont(self.create_font(font_size=font_size))
            self.ComboBoxItems.update({self.ComboBoxes[object_name]: {}})
            self.ComboBoxes[object_name].show() if visible else self.ComboBoxes[object_name].hide()
            for item in items:
                local_var = len(self.ComboBoxItems[self.ComboBoxes[object_name]])
                self.ComboBoxItems[self.ComboBoxes[object_name]].update({local_var: item})
                self.ComboBoxes[object_name].addItem(item)
            if css: self.ComboBoxes[object_name].setStyleSheet\
                (f"border-style:{border_style}; border-width:{border_width}px; border-color:{border_color}; background-color:rgb{rgb};")

    def on_CurrentIndexChanged(self, i):
        print(f" <{i}> | <{self.ComboBoxItems[self.sender()][i]}>")
# -------------------------------------------------------------------------------------------------------------------- #
    def setup_GroupBoxes(self):
        self.add_GroupBox("RightBottomButtons", evaloc(4, 9, width=2), visible=False, css=False, borderless=True)
        self.add_GroupBox("RDTemplate", evaloc(2, 1, width=5), visible=False, borderless=True)
        self.add_GroupBox("RDPart", evaloc(4, 1, width=2), visible=False, borderless=True)
        self.add_GroupBox("RenameTemplate", evaloc(2, 1, case=1), GroupBox="RDTemplate", css=True)
        self.add_GroupBox("RenamePart", evaloc(1, 1, case=1), GroupBox="RDPart", css=True)

    def add_GroupBox(self, object_name, geometry, GroupBoxText=None, GroupBox=None, Tab=None, borderless=False, visible=True, css=True, rgb=(255, 255, 255)):
        parent = self.decideFunction_0(GroupBox, Tab)
        widgetType = (QFrame(parent) if borderless else QGroupBox(parent))
        x, y, width, height = geometry
        if object_name not in self.GroupBoxes:
            self.GroupBoxes.update({object_name: widgetType})
            self.GroupBoxes[object_name].setGeometry(QRect(x, y, width, height))
            self.GroupBoxes[object_name].show() if visible else self.GroupBoxes[object_name].hide()
            if not borderless:
                if css: self.GroupBoxes[object_name].setStyleSheet(f"border-style:solid; border-width:1px; border-color:black; background-color:rgb{rgb};")
                if GroupBoxText is not None: self.GroupBoxes[object_name].setTitle(GroupBoxText)
# -------------------------------------------------------------------------------------------------------------------- #
    def setup_LineEdits(self):
        self.add_LineEdit("TemplateName", "", (92, 0, 91, 50), GroupBox="RenameTemplate", target=self.rename_template, rgb=(250, 175, 175), font_size=12)
        self.add_LineEdit("PartName", "", (92, 0, 91, 50), GroupBox="RenamePart", target=self.rename_part, rgb=(250, 175, 175), font_size=12)

    def add_LineEdit(self, object_name, object_text, geometry, font_size=10, GroupBox=None, Tab=None, visible=True, target=None, center=True, arg=None, rgb=(175, 220, 220)):
        parent = self.decideFunction_0(GroupBox, Tab)
        x, y, width, height = geometry
        if object not in self.LineEdits:
            self.LineEdits.update(
                {object_name: QLineEdit(object_text, self if GroupBox is None else self.GroupBoxes[GroupBox])})
            self.LineEdits[object_name].setGeometry(QRect(x, y, width, height))
            self.LineEdits[object_name].setFont(self.create_font(font_size=font_size))
            self.LineEdits[object_name].setStyleSheet(f"background-color:rgb{rgb};")
            self.LineEdits[object_name].show() if visible else self.LineEdits[object_name].hide()
            if target is not None: self.LineEdits[object_name].textChanged.connect(target)
            if center: self.LineEdits[object_name].setAlignment(Qt.AlignCenter)

    def int_input(self):
        text = (self.sender()).text()
        if len(text) != 0:
            for letter in text:
                if letter not in digits:
                    i = text.find(letter)
                    text = text[:i] + text[i+1:]
                    (self.sender()).setText(text)
        if len(text) > 1:
            if text[0] == "0":
                text = text[1:]
                (self.sender()).setText(text)

# -------------------------------------------------------------------------------------------------------------------- #
    def setup_Labels(self):
        self.add_Label("RenameTemplate", "Şablon Adı:", (0, 0, 92, 50), GroupBox="RenameTemplate", rgb=(243, 91, 104), font_size=12)
        self.add_Label("RenamePart", "Parça Adı:", (0, 0, 92, 50), GroupBox="RenamePart", rgb=(243, 91, 104), font_size=12)

    def add_Label(self, object_name, object_text, geometry, font_size=10, GroupBox=None, Tab=None, visible=True,
                  center=True, css=True, rgb=(100, 205, 205), border_style='solid', border_width='1', border_color='black'):
        parent = self.decideFunction_0(GroupBox, Tab)
        x, y, width, height = geometry
        if object_name not in self.Labels:
            parent = self if GroupBox is None else self.GroupBoxes[GroupBox]
            self.Labels.update({object_name: QLabel(object_text, parent)})
            self.Labels[object_name].setGeometry(QRect(x, y, width, height))
            self.Labels[object_name].setFont(self.create_font(font_size=font_size))
            self.Labels[object_name].show() if visible else self.Labels[object_name].hide()
            if center: self.Labels[object_name].setAlignment(Qt.AlignCenter)
            if css: self.Labels[object_name].setStyleSheet\
                (f"border-style:{border_style}; border-width:{border_width}px; border-color:{border_color};background-color:rgb{rgb};")
# -------------------------------------------------------------------------------------------------------------------- #
    def setup_Tabs(self):
        self.add_Tab("MainTab", (235, 103, 1019, 513), visible=False)
        self.setup_Tab1()
        self.setup_Tab2()
        self.setup_Tab3()
        self.setup_Tab4()
        self.setup_Tab5()

    def add_Tab(self, object_name, geometry, GroupBox=None, visible=True, font_size=10, css=True,
                rgb=(248, 248, 248), border_style='solid', border_width='1', border_color='gray'):
        x, y, width, height = geometry
        if object_name not in self.Tabs:
            parent = self if GroupBox is None else self.GroupBoxes[GroupBox]
            self.Tabs.update({object_name: QTabWidget(parent)})
            self.Tabs[object_name].setGeometry(QRect(x, y, width, height))
            self.Tabs[object_name].setFont(self.create_font(font_size=font_size))
            self.Tabs[object_name].show() if visible else self.Tabs[object_name].hide()
            if css: self.Tabs[object_name].setStyleSheet\
                (f"border-style:{border_style}; border-width:{border_width}px; border-color:{border_color}; background-color:rgb(225, 240, 255);")

    def add_Widget(self, object_text, tab):
        self.Tabs.update({object_text: QWidget(self.Tabs[tab])})
        self.Tabs[tab].addTab(self.Tabs[object_text], object_text)
# -------------------------------------------------------------------------------------------------------------------- #
    def setup_Tab1(self):
        self.add_Widget("Grafik", "MainTab")
        self.add_GroupBox("Graph", (26, 26, 961, 431), Tab="Grafik", GroupBoxText="Grafik", rgb=(220, 245, 245))

        self.add_GroupBox("GraphTypes", (177, 70, 200, 30), GroupBox="Graph", borderless=True)
        self.add_Label("GraphType", "Grafik Türü:", (0, 0, 100, 30), GroupBox="GraphTypes")
        self.add_ComboBox("GraphType", (100, 0, 100, 30), ("Daire Grafiği", "Bar Grafiği", "Konum Grafiği"), self.on_CurrentIndexChanged, GroupBox="GraphTypes")

        self.add_GroupBox("graph_name", (177, 170, 200, 30), GroupBox="Graph", borderless=True)
        self.add_Label("graph_name", "Grafik Adı:", (0, 0, 100, 30), GroupBox="graph_name")
        self.add_LineEdit("graph_name", "", (100, 0, 100, 30), GroupBox="graph_name")

        self.add_GroupBox("variable_unit", (177, 270, 200, 30), GroupBox="Graph", borderless=True)
        self.add_Label("variable_unit", "Birim:", (0, 0, 100, 30), GroupBox="variable_unit")
        self.add_LineEdit("variable_unit", "", (100, 0, 100, 30), GroupBox="variable_unit")

        self.add_GroupBox("show_minimum_value", (554, 270, 230, 30), rgb=(175, 220, 220), GroupBox="Graph")
        self.add_Label("show_minimum_value", "Minimum Değeri Göster:", (0, 0, 200, 30), GroupBox="show_minimum_value")
        self.add_CheckBox("show_minimum_value", "", (208, 2, 13, 26), GroupBox="show_minimum_value")

        self.add_GroupBox("show_average_value", (554, 170, 230, 30), rgb=(175, 220, 220), GroupBox="Graph")
        self.add_Label("show_average_value", "Ortalama Değeri Göster:", (0, 0, 200, 30), GroupBox="show_average_value")
        self.add_CheckBox("show_average_value", "", (208, 2, 13, 26), GroupBox="show_average_value")

        self.add_GroupBox("show_maximum_value", (554, 70, 230, 30), rgb=(175, 220, 220), GroupBox="Graph")
        self.add_Label("show_maximum_value", "Maksimum Değeri Göster:", (0, 0, 200, 30), GroupBox="show_maximum_value")
        self.add_CheckBox("show_maximum_value", "", (208, 2, 13, 26), GroupBox="show_maximum_value")

        text_GraphInfo = "*Grafik: Grafiğin çeşidi ve grafik üzerinde gösterilecek bazı değerler ile ilgili değişikler bu sekmeden yapılır."
        self.add_Label("GraphInfo", text_GraphInfo, (0, 371, 961, 60), rgb=(190, 230, 220), GroupBox="Graph")

    def setup_Tab2(self):
        self.add_Widget("Geometri", "MainTab")
        self.add_GroupBox("Geometry", (26, 26, 961, 431), Tab="Geometri", GroupBoxText="Geometri", rgb=(220, 245, 245))
        self.add_Label("x", "x:", (26, 26, 100, 30), GroupBox="Geometry")
        self.add_LineEdit("x", "", (126, 26, 100, 30), GroupBox="Geometry", target=self.int_input)
        self.add_Label("y", "y:", (380, 26, 100, 30), GroupBox="Geometry")
        self.add_LineEdit("y", "", (480, 26, 100, 30), GroupBox="Geometry", target=self.int_input)
        self.add_Label("frame_width", "Çerçeve kalınlığı:", (735, 26, 100, 30), GroupBox="Geometry")
        self.add_LineEdit("frame_width", "", (835, 26, 100, 30), GroupBox="Geometry", target=self.int_input)
        self.add_Label("width", "Genişlik:", (205, 126, 100, 30), GroupBox="Geometry")
        self.add_LineEdit("width", "", (305, 126, 100, 30), GroupBox="Geometry", target=self.int_input)
        self.add_Label("height", "Yükseklik:", (559, 126, 100, 30), GroupBox="Geometry")
        self.add_LineEdit("height", "", (659, 126, 100, 30), GroupBox="Geometry", target=self.int_input)
        text_GeometryInfo = "*Geometri: Grafiğin çizileceği konum (x, y) ve grafiğin boyutu (genişlik, yükseklik, çerçeve kalınlığı) ile ilgili değişiklikler bu sekmeden yapılır." \
                            "\nBu sayfadaki tüm değişkenler piksel (px) cinsindendir ve ancak tam sayı olarak girilebilir."
        self.add_Label("GeometryInfo", text_GeometryInfo, (0, 371, 961, 60), rgb=(190, 230, 220), GroupBox="Geometry")

    def setup_Tab3(self):
        self.add_Widget("Ölçeklendirme", "MainTab")
        self.add_GroupBox("Scaling", (26, 26, 961, 431), Tab="Ölçeklendirme", GroupBoxText="Ölçeklendirme", rgb=(220, 245, 245))
        self.add_Label("minimum_value", "Min. Değer:", (177, 270, 100, 30), GroupBox="Scaling")
        self.add_LineEdit("minimum_value", "", (277, 270, 100, 30), GroupBox="Scaling")
        self.add_Label("maximum_value", "Maks. Değer:", (177, 170, 100, 30), GroupBox="Scaling")
        self.add_LineEdit("maximum_value", "", (277, 170, 100, 30), GroupBox="Scaling")
        self.add_Label("scale_lines_count", "Ayraç Sayısı:", (177, 70, 100, 30), GroupBox="Scaling")
        self.add_LineEdit("scale_lines_count", "", (277, 70, 100, 30), GroupBox="Scaling", target=self.int_input)

        self.add_GroupBox("show_minimum_line", (554, 270, 230, 30), rgb=(175, 220, 220), GroupBox="Scaling")
        self.add_Label("show_minimum_line", "Minimum Değer Çizgisini Göster:", (0, 0, 200, 30), GroupBox="show_minimum_line")
        self.add_CheckBox("show_minimum_line", "", (208, 2, 13, 26), GroupBox="show_minimum_line")

        self.add_GroupBox("show_average_line", (554, 170, 230, 30), rgb=(175, 220, 220), GroupBox="Scaling")
        self.add_Label("show_average_line", "Ortalama Değer Çizgisini Göster:", (0, 0, 200, 30), GroupBox="show_average_line")
        self.add_CheckBox("show_average_line", "", (208, 2, 13, 26), GroupBox="show_average_line")

        self.add_GroupBox("show_maximum_line", (554, 70, 230, 30), rgb=(175, 220, 220), GroupBox="Scaling")
        self.add_Label("show_maximum_line", "Maksimum Değer Çizgisini Göster:", (0, 0, 200, 30), GroupBox="show_maximum_line")
        self.add_CheckBox("show_maximum_line", "", (208, 2, 13, 26), GroupBox="show_maximum_line")

        text_ScalingInfo = "*Ölçeklendirme: Grafiğin hangi değer aralığında (minimum değer, maksimum değer) çizileceği ve bu değer aralığının kaça (ayraç sayısı) ayrılacağı ile ilgili değişiklikler" \
                           "\nbu sekmeden yapılır. 'Minimum Değer' ve 'Maksimum Değer' ondalıklı veya tam sayı olabilir fakat 'Ayraç Sayısı' ancak tam sayı olarak girilebilir."
        self.add_Label("ScalingInfo", text_ScalingInfo, (0, 371, 961, 60), rgb=(190, 230, 220), GroupBox="Scaling")

    def setup_Tab4(self):
        self.add_Widget("Dosya", "MainTab")
        self.add_GroupBox("File", (26, 26, 961, 431), Tab="Dosya", GroupBoxText="Dosya", rgb=(220, 245, 245))
        self.add_Label("file_directory", "Dosya Dizini:", (26, 26, 100, 30), GroupBox="File")
        self.add_LineEdit("file_directory", "", (126, 26, 100, 30), GroupBox="File")
        self.add_Label("index", "İndeks:", (380, 26, 100, 30), GroupBox="File")
        self.add_LineEdit("index", "", (480, 26, 100, 30), GroupBox="File", target=self.int_input)
        self.add_Label("split_by", "Ayraç:", (735, 26, 100, 30), GroupBox="File")
        self.add_LineEdit("split_by", "", (835, 26, 100, 30), GroupBox="File")
        text_FileInfo = "*Dosya: Grafik üzerinde gösterilecek olan verinin hangi dosyadan (dosya dizini) çekileceği, bu verinin dosya içerisinde ne ile (ayraç) ayıklanacağı ve bu verinin" \
                            "\nsatır üzerinde kaçıncı sırada (indeks) yer aldığı bilgisi ile ilgili değişiklikler bu sekmeden yapılır. 'İndeks' ancak tam sayı olarak girilebilir."
        self.add_Label("FileInfo", text_FileInfo, (0, 371, 961, 60), rgb=(190, 230, 220), GroupBox="File")

    def setup_Tab5(self):
        self.add_Widget("Renkler", "MainTab")
        self.add_GroupBox("Colors", (26, 26, 961, 431), Tab="Renkler", GroupBoxText="Renkler", rgb=(220, 245, 245))
        self.add_Label("bar_color", "Grafik Rengi:", (203, 70, 100, 30), GroupBox="Colors")
        self.add_LineEdit("bar_color", "", (303, 70, 100, 30), GroupBox="Colors")
        self.add_Label("frame_color", "Çerçeve Rengi:", (557, 70, 100, 30), GroupBox="Colors")
        self.add_LineEdit("frame_color", "", (657, 70, 100, 30), GroupBox="Colors")
        self.add_Label("minimum_value_color:", "Min. D. Rengi:", (26, 170, 100, 30), GroupBox="Colors")
        self.add_LineEdit("minimum_value_color", "", (126, 170, 100, 30), GroupBox="Colors")
        self.add_Label("average_value_color", "Ort. D. Rengi:", (380, 170, 100, 30), GroupBox="Colors")
        self.add_LineEdit("average_value_color", "", (480, 170, 100, 30), GroupBox="Colors")
        self.add_Label("maximum_value_color", "Maks. D. Rengi:", (735, 170, 100, 30), GroupBox="Colors")
        self.add_LineEdit("maximum_value_color", "", (835, 170, 100, 30), GroupBox="Colors")
        self.add_Label("graph_name_color", "Grafik Adı Rengi:", (203, 270, 100, 30), GroupBox="Colors")
        self.add_LineEdit("graph_name_color", "", (303, 270, 100, 30), GroupBox="Colors")
        self.add_Label("current_value_color", "Birim Rengi:", (557, 270, 100, 30), GroupBox="Colors")
        self.add_LineEdit("current_value_color", "", (657, 270, 100, 30), GroupBox="Colors")
        text_ColorsInfo = "*Renkler: Grafiğin rengi ile ilgili değişiklikler bu sekmeden yapılır. (Min. D. = Minimum Değer, Ort. D. = Ortalam Değer, Maks. D. = Maksimum Değer)" \
                          "\nMevcut seçenekler: kırmızı, yeşil, mavi, turkuaz, sarı, turuncu, mor, siyah, beyaz."
        self.add_Label("ColorsInfo", text_ColorsInfo, (0, 371, 961, 60), rgb=(190, 230, 220), GroupBox="Colors")
# -------------------------------------------------------------------------------------------------------------------- #
    def setup_Templates(self):
        self.Templates = QTreeWidget(self)
        self.Templates.setGeometry(QRect(26, 103, 183, 513))
        self.Templates.setStyleSheet("background-color:rgb(225, 240, 255);")
        self.Templates.setFrameStyle(1)
        self.Templates.setFont(self.create_font(12))
        self.Templates.setHeaderHidden(True)
        self.Templates.show()
        self.Templates.itemClicked.connect(self.on_ItemClicked)
        self.Templates_Title = QTreeWidgetItem(self.Templates)
        self.selected_template, self.selected_part = None, None
        self.update_TPnI()

        self.default_BarGraph = ["GraphType|Bar Grafiği", "graph_name|Mesafe Ölçer", "variable_unit|cm", "x|150", "y|150", "width|100",
                                 "height|400", "frame_width|24", "minimum_value|0", "maximum_value|100", "scale_lines_count|10",
                                 "bar_color|kırmızı", "frame_color|siyah", "maximum_value_color|turkuaz", "average_value_color|sarı", "minimum_value_color|yeşil", "current_value_color|beyaz", "graph_name_color|kırmızı",
                                 "file_directory|", "index|0", "split_by|:",
                                 "show_minimum_value|False", "show_average_value|False", "show_maximum_value|False",
                                 "show_minimum_line|False", "show_average_line|False", "show_maximum_line|False"]

        self.BarGraphProperties = {"GraphType": "Bar Grafiği", "graph_name": None, "variable_unit": None, "x": None, "y": None, "width": None,
                                   "height": None, "frame_width": None, "minimum_value": None, "maximum_value": None, "scale_lines_count": None,
                                   "bar_color": None, "frame_color": None, "maximum_value_color": None, "average_value_color": None,
                                   "minimum_value_color": None, "current_value_color": None, "graph_name_color": None,
                                   "file_directory": None, "index": None, "split_by": None,
                                   "show_minimum_value": None, "show_average_value": None, "show_maximum_value": None,
                                   "show_minimum_line": None, "show_average_line": None, "show_maximum_line": None}

    def update_TPnI(self):
        def clear():
            self.Templates.clear()
            self.templates.clear()
            self.TemplateItems.clear()
            self.PartItems.clear()

        def update_Templates():
            for template in os.listdir(path=r".\bin\Şablonlar"):
                parts = os.listdir(path=r".\bin\Şablonlar\{0}".format(template))
                self.templates.update({template: list((part.strip(".txt") for part in parts))})

        def update_Items():
            for template in self.templates:
                self.TemplateItems.update({template: QTreeWidgetItem([template])})
                self.TemplateItems[template].setBackgroundColor(0, qRgb(195, 215, 240))
                self.Templates.addTopLevelItem(self.TemplateItems[template])
                for part in self.templates[template]:
                    self.PartItems.update({f"{template}_{part}": QTreeWidgetItem([part])})
                    self.TemplateItems[template].addChild(self.PartItems[f"{template}_{part}"])
                    self.PartItems[f"{template}_{part}"].setBackgroundColor(0, qRgb(210, 230, 250))

        def procedure():
            clear()
            update_Templates()
            update_Items()
            if self.selected_template is not None and self.selected_template in self.TemplateItems: self.TemplateItems[self.selected_template].setExpanded(True)

        procedure()

    def select(self, object_name, case):
        for item in self.Templates.selectedItems(): item.setSelected(False)
        if case == "Part":
            self.PartItems[f"{self.selected_template}_{object_name}"].setSelected(True)
            self.selected_part = object_name
            self.selected_new_part()
        elif case == "Template":
            self.TemplateItems[object_name].setSelected(True)
            self.selected_template = object_name
            self.selected_new_template()

    def generate_name(self, case, number=0):
        if case == 'Part': object_type, dictionary = 'Parça', self.templates[self.selected_template]
        else: object_type, dictionary = 'Şablon', self.templates
        object_name = f"{object_type}_{number}"
        if object_name in dictionary: return self.generate_name(case, number=number + 1)
        else: return object_name

    def create_template(self):
        template_name = self.generate_name(case='Template')
        os.mkdir(r".\bin\Şablonlar\{0}".format(template_name))
        self.update_TPnI()
        self.select(template_name, case="Template")

    def create_part(self):
        part_name = self.generate_name(case='Part')
        file = open(r".\bin\Şablonlar\{0}\{1}.txt".format(self.selected_template, part_name), "x")
        for line in self.default_BarGraph:
            file.write(line+"\n")
        file.close()
        self.update_TPnI()
        self.select(part_name, case="Part")

    def rename_template(self):
        old_name = self.selected_template
        new_name = (self.sender()).text()
        if new_name not in self.templates and len(new_name) != 0:
            try:
                os.rename(r".\bin\Şablonlar\{0}".format(old_name),
                          r".\bin\Şablonlar\{0}".format(new_name))
                self.update_TPnI()
                self.select(new_name, case="Template")
            except (FileExistsError, OSError) as exception:
                (self.sender()).setText(old_name)
                pass

    def rename_part(self):
        old_name = self.selected_part
        new_name = (self.sender()).text()
        if new_name not in self.templates[self.selected_template] and len(new_name) != 0:
            try:
                os.rename(r".\bin\Şablonlar\{0}\{1}.txt".format(self.selected_template, old_name),
                          r".\bin\Şablonlar\{0}\{1}.txt".format(self.selected_template, new_name))
                self.update_TPnI()
                self.select(new_name, case="Part")
            except (FileExistsError, OSError) as exception:
                (self.sender()).setText(old_name)
                pass

    def delete_template(self):
        if self.selected_template is not None:
            shutil.rmtree(r".\bin\Şablonlar\{0}".format(self.selected_template))
            self.GroupBoxes["RightBottomButtons"].hide()
            self.GroupBoxes["RDTemplate"].hide()
            self.GroupBoxes["RDPart"].hide()
            self.PushButtons["Run"].hide()
            self.Tabs["MainTab"].hide()
            self.update_TPnI()

    def delete_part(self):
        if self.selected_part is not None:
            os.remove(r".\bin\Şablonlar\{0}\{1}.txt".format(self.selected_template, self.selected_part))
            self.GroupBoxes["RightBottomButtons"].hide()
            self.GroupBoxes["RDPart"].hide()
            self.PushButtons["Run"].hide()
            self.Tabs["MainTab"].hide()
            self.update_TPnI()

    def selected_new_template(self):
        if self.selected_template in self.templates: self.TemplateItems[self.selected_template].setExpanded(True)
        self.LineEdits["TemplateName"].setText(self.selected_template)
        self.GroupBoxes["RDTemplate"].show()
        self.PushButtons["Run"].show()
        self.GroupBoxes["RightBottomButtons"].hide()
        self.GroupBoxes["RDPart"].hide()
        self.Tabs["MainTab"].hide()

    def selected_new_part(self):
        for template in self.templates:
            if self.selected_part in self.templates[template]:
                if self.Templates.isItemSelected(self.PartItems[f"{template}_{self.selected_part}"]):
                    self.selected_template = template
                    self.LineEdits["TemplateName"].setText(self.selected_template)
                    self.LineEdits["PartName"].setText(self.selected_part)
                    self.GroupBoxes["RightBottomButtons"].show()
                    self.GroupBoxes["RDTemplate"].show()
                    self.GroupBoxes["RDPart"].show()
                    self.PushButtons["Run"].show()
                    self.Tabs["MainTab"].show()
                    self.update_PartItems_in_Tab()

    def update_PartItems_in_Tab(self):
        lines = open(r".\bin\Şablonlar\{0}\{1}.txt".format(self.selected_template, self.selected_part), "r", encoding="ANSI").readlines()
        for i in range(len(lines)):
            lines[i] = (lines[i])[:len(lines[i])-1]
        for line in lines:
            line = line.split("|")
            self.BarGraphProperties.update({line[0]: line[1]})
            if line[0] in self.LineEdits:
                self.LineEdits[line[0]].setText(line[1])
            elif line[0] in self.ComboBoxes:
                for key in self.ComboBoxItems:
                    for i in self.ComboBoxItems[key]:
                        dictionary = self.ComboBoxItems[key]
                        if line[1] == dictionary[i]:
                            self.ComboBoxes[line[0]].setCurrentIndex(i)
            elif line[0] in self.CheckBoxes:
                if line[1] == "1" or line[1] == 1: self.CheckBoxes[line[0]].setChecked(True)
                else: self.CheckBoxes[line[0]].setChecked(False)

    def on_ItemClicked(self):
        sender = (self.Templates.selectedItems())[0].text(0)
        if sender in self.templates:
            self.selected_template = sender
            self.selected_new_template()
        else:
            self.selected_part = sender
            self.selected_new_part()

    def update_BarGraphProperties(self):
        dictionary = self.BarGraphProperties
        for key in dictionary:
            if key in self.LineEdits:
                dictionary[key] = self.LineEdits[key].text()
            elif key in self.ComboBoxes:
                dictionary[key] = self.ComboBoxes[key].currentText()
            elif key in self.CheckBoxes:
                checked = self.CheckBoxes[key].isChecked()
                if checked: dictionary[key] = 1
                else: dictionary[key] = 0

    def on_clicked_save_button(self):
        local_graph_type = self.ComboBoxes["GraphType"].currentText()
        dictionary = None
        if local_graph_type == "Bar Grafiği":
            self.update_BarGraphProperties()
            dictionary = self.BarGraphProperties
        if dictionary is not None:
            file = open(r".\bin\Şablonlar\{0}\{1}.txt".format(self.selected_template, self.selected_part), "w", encoding="ANSI")
            for key in dictionary:
                string_to_write = key + "|" + str(dictionary[key]) + "\n"
                file.write(string_to_write)

    def on_clicked_redo_button(self):
        self.update_PartItems_in_Tab()

    def on_clicked_run_button(self):
        gui.PushButtons["Run"].setDisabled(True)
        VP.start()
        Graphs.setup_Graphs()
        Threads.setup_all()

# -------------------------------------------------------------------------------------------------------------------- #
colors = {"siyah": (0, 0, 0), "beyaz": (255, 255, 255), "kırmızı": (250, 0, 0), "yeşil": (0, 255, 0), "mavi": (0, 0, 255),
          "gri": (122, 122, 122), "sarı": (255, 255, 0), "turkuaz": (0, 255, 255), "mor": (255, 0, 255), "bg": (170, 170, 170),
          "turuncu": (255, 50, 50)}

class Threads:
    def __init__(self):
        self.dictionary_threads = {}
        self.list_check = []
        self.dictionary_status = {}

    def setup_all(self):
        self.setup_status()
        self.setup_threads()
        self.setup_check()

    def setup_status(self):
        pass

    def setup_threads(self):
        self.add("VP.update_constantly", VP.update_constantly)
        self.add("Graphs.check_all", Graphs.check_all)
        self.add("control_VisualizationPart", control_VisualizationPart)

    def setup_check(self):
        pass

    def update_dictionary(self, text, target, dictionary):
        dictionary.update({text: target})

    def remove_from_dictionary(self, text, dictionary):
        dictionary.pop(text)

    def add(self, text, target, start=True):
        self.dictionary_threads.update({text: threading.Thread(target=target)})
        self.update_dictionary(text, True, self.dictionary_status)
        if start: self.dictionary_threads[text].start()

    def stop(self, key):
        if key in self.dictionary_status: self.dictionary_status.update({key: False})

class VisualizationPart:
    def __init__(self, width, height, full_screen=False, background_color="bg", text_color="yeşil"):
        self.stop = False
        self.full_screen = full_screen
        self.width, self.height = width, height
        self.background_color = colors[background_color]
        self.prev_s = 0
        self.text_color = text_color

    def start(self):
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN if self.full_screen else 0)
        pygame.init()
        pygame.font.init()
        self.initial_time = time.perf_counter()

    def update(self):
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def update_constantly(self, fps=30):
        while Threads.dictionary_status["VP.update_constantly"]:
            time.sleep(1/fps)
            self.fill()
            Graphs.draw_all()
            self.update()

    def fill(self):
        self.screen.fill(self.background_color)

    def draw_texts(self):  # Şimdilik devre dışı
        current_time = time.perf_counter()
        elapsed_time = round(current_time - self.initial_time, 1)
        latency = round(current_time - self.prev_s, 4)
        self.prev_s = current_time
        text_time_elapsed = self.font.render(f"Geçen Zaman | {elapsed_time}", True, colors[self.text_color])
        text_latency = self.font.render(f"Gecikme | {latency}", True, colors[self.text_color])
        self.screen.blit(text_time_elapsed, (0, 0))
        self.screen.blit(text_latency, (0, 32))


class Graphs:
    def __init__(self):
        self.dictionary = {}

    def setup_Graphs(self):
        args = []
        for part in gui.templates[gui.selected_template]:
            lines = open(r".\bin\Şablonlar\{0}\{1}.txt".format(gui.selected_template, part), "r").readlines()
            for line in lines:
                line = line.split("|")
                line[1] = (line[1])[:len(line[1])-1]
                try:
                    if "." in line[1]: line[1] = float(line[1])
                    else: line[1] = int(line[1])
                except (TypeError, ValueError) as exception:
                    str(line[1])
                args.append(line[1])
            Bar(args)
            args.clear()

    def draw_all(self):
        for graph_name in self.dictionary:
            (self.dictionary[graph_name]).draw()

    def check_all(self, delay=1):
        while Threads.dictionary_status["Graphs.check_all"]:
            for graph_name in self.dictionary:
                (self.dictionary[graph_name]).check()
            time.sleep(delay)


class Bar:
    def __init__(self, args):
        args.append(32)
        self.setup_all(args=args)

    def setup_all(self, args):
        self.setup_variables(args=args)
        self.setup_miscellaneous()

    def setup_miscellaneous(self):
        self.font = pygame.font.SysFont("Monospace", self.font_size)
        self.line_number = 0
        self.initial_time = time.perf_counter()
        self.lines_count, self.old_lines_count = 0, 0
        Graphs.dictionary.update({self.graph_name: self})
        self.first_check()
        self.create_scale_texts()

    def setup_variables(self, args):
        self.graph_name, self.variable_unit = args[1], args[2]
        self.x, self.y, self.width, self.height = args[3], args[4], args[5], args[6]
        self.frame_width = args[7]
        self.minimum_value, self.maximum_value, self.scale_lines_count = args[8], args[9], args[10]
        self.bar_color = colors[args[11]]
        self.frame_color = colors[args[12]]
        self.maximum_value_color = colors[args[13]]
        self.average_value_color = colors[args[14]]
        self.minimum_value_color = colors[args[15]]
        self.current_value_color = colors[args[16]]
        self.graph_name_color = colors[args[17]]
        self.file_directory, self.index, self.split_by = args[18], args[19], args[20]
        self.show_minimum_value = args[21]
        self.show_average_value = args[22]
        self.show_maximum_value = args[23]
        self.show_minimum_value_line = args[24]
        self.show_average_value_line = args[25]
        self.show_maximum_value_line = args[26]
        self.font_size = args[27]

    def first_check(self):  # Test (Simülasyon) Modu için gerekli.
        self.variable = round(random.uniform(self.minimum_value, self.maximum_value), 2)
        self.min = self.variable
        self.avg = self.variable
        self.max = self.variable
        self.total = self.variable
        self.num_of_elements = 1

    def check2(self):  # Normal kullanım için. (Test edilmedi).
        lines = open(self.file_directory, "r").readlines()
        self.lines_count = len(lines)
        if self.lines_count > self.old_lines_count:
            self.num_of_elements += 1
            self.variable = ((lines[self.lines_count]).split(self.split_by))[self.index]
            if self.num_of_elements == 1: self.min, self.max, self.total = self.variable, self.variable, self.variable
            if self.variable < self.min: self.min = self.variable
            if self.variable > self.max: self.max = self.variable
            self.total += self.variable
            self.avg = self.total / self.num_of_elements

    def check(self):  # Test (Simülasyon) Modu için gerekli.
        self.variable = round(random.uniform(self.minimum_value, self.maximum_value), 2)
        if self.variable < self.min: self.min = self.variable
        if self.variable > self.max: self.max = self.variable
        self.total += self.variable
        self.num_of_elements += 1
        self.avg = self.total / self.num_of_elements

    def draw_frame(self):
        pygame.draw.rect(VP.screen, self.frame_color, [self.x - self.frame_width // 2, self.y - self.frame_width // 2, self.width + self.frame_width, self.height + self.frame_width])  # Frame
        pygame.draw.rect(VP.screen, VP.background_color, [self.x, self.y, self.width, self.height])  # Background

    def draw_bar(self):
        pos_height = int(self.height * (self.variable - self.minimum_value) / (self.maximum_value - self.minimum_value))
        pygame.draw.rect(VP.screen, self.bar_color, [self.x, self.y + self.height - pos_height, self.width, pos_height])  # The bar itself

    def create_scale_texts(self):  # Bu fonksiyon tamamiyle darmadağınık. (Ama çalışıyor.)
        value = (self.maximum_value - self.minimum_value) / self.scale_lines_count
        self.scaling_texts = []
        slc = self.scale_lines_count
        local_list = []
        type_list = []

        for n in range(self.scale_lines_count + 1):
            text_value = str(round(self.maximum_value - n * value, 2))
            if (text_value.split("."))[1] == "0": text_value = int(float(text_value))
            local_list.append(str(text_value))
            type_list.append(type(text_value))

        if str in type_list:
            mtc = max(list(len((str(round(self.maximum_value - n * value, 2)).split("."))[1]) for n in range(slc + 1)))
            for n in range(slc + 1):
                text_value = str(round(self.maximum_value - n * value, 2))
                if (text_value.split("."))[1] == "0": text_value = int(float(text_value))
                if type(text_value) == int: text_value = str(text_value) + "." + "0" * mtc
                elif "." in text_value and len((text_value.split("."))[1]) != mtc: text_value = text_value + "0"
                self.scaling_texts.append(str(text_value))
        else:
            self.scaling_texts = local_list

    def draw_scale_texts(self):  # Şimdilik ölçek çizgisi olarak metin içerisindeki kısa çizgiler (-) kullanılıyor. (Beraberinde bir takım sorunlar da getiriyor.)
        position_y = self.height // self.scale_lines_count
        for n in range(self.scale_lines_count + 1):
            text = self.font.render(f"-{self.scaling_texts[n]}", True, (255, 255, 255))
            VP.screen.blit(text, (self.x + self.width - 3, self.y + n * position_y - (self.font_size//2 + 2)))

    def show_values_on_graph(self):
        if self.show_maximum_value_line:
            pos_max = int(self.height * (self.max - self.minimum_value) / (self.maximum_value - self.minimum_value)) + 3
            pygame.draw.rect(VP.screen, self.minimum_value_color, [self.x, self.y + self.height - pos_max, self.width, 5])  # Max
            text_max = self.font.render(f"max", True, self.minimum_value_color)
            VP.screen.blit(text_max, (self.x - 75, self.y + self.height - pos_max - 15))
        if self.show_average_value_line:
            pos_avg = int(self.height * (self.avg - self.minimum_value) / (self.maximum_value - self.minimum_value)) + 3
            pygame.draw.rect(VP.screen, self.average_value_color, [self.x, self.y + self.height - pos_avg, self.width, 5])  # Average
            text_avg = self.font.render(f"Ort", True, self.average_value_color)
            VP.screen.blit(text_avg, (self.x - 75, self.y + self.height - pos_avg - 15))
        if self.show_minimum_value_line:
            pos_min = int(self.height * (self.min - self.minimum_value) / (self.maximum_value - self.minimum_value)) + 3
            pygame.draw.rect(VP.screen, self.maximum_value_color, [self.x, self.y + self.height - pos_min, self.width, 5])  # Min
            text_min = self.font.render(f"min", True, self.maximum_value_color)
            VP.screen.blit(text_min, (self.x - 75, self.y + self.height - pos_min - 15))

    def show_values_as_text(self):
        x, y = self.x - 10, self.y + self.height + 10
        local_list = [self.show_maximum_value, self.show_average_value, self.show_minimum_value]
        local_variable = self.font_size//2 + 9
        if self.show_maximum_value:
            text_var_max = self.font.render(f"Max: {self.max}", True, self.minimum_value_color)
            VP.screen.blit(text_var_max, (x, y))
        if self.show_average_value:
            text_var_avg = self.font.render(f"Ort: {round(self.avg, 2)}", True, self.average_value_color)
            VP.screen.blit(text_var_avg, (x, y + local_variable * sum(local_list[:1])))
        if self.show_minimum_value:
            text_var_min = self.font.render(f"Min: {self.min}", True, self.maximum_value_color)
            VP.screen.blit(text_var_min, (x, y + local_variable * sum(local_list[:2])))
        text_var_current = self.font.render(f"{self.variable} {self.variable_unit}", True, self.current_value_color)
        text_graph_name = self.font.render(self.graph_name, True, self.graph_name_color)
        VP.screen.blit(text_graph_name, (x, y + local_variable * sum(local_list[:3])))
        VP.screen.blit(text_var_current, (x, y + local_variable * (sum(local_list[:3]) + 1)))


    def procedure_draw(self):
        self.draw_frame()
        self.draw_bar()
        self.draw_scale_texts()
        self.show_values_on_graph()
        self.show_values_as_text()

    def draw(self):
        if self.variable is not None: self.procedure_draw()

def control_VisualizationPart():
    try:
        while Threads.dictionary_status["control_VisualizationPart"]:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        for key in Threads.dictionary_status:
                            Threads.dictionary_status[key] = False
                        Graphs.dictionary.clear()
                        Threads.dictionary_threads.clear()
                        pygame.quit()
            time.sleep(1 / 100)
    except pygame.error:
        pass
    time.sleep(2)
    Threads.dictionary_status.clear()
    gui.PushButtons["Run"].setDisabled(False)

Threads = Threads()
Graphs = Graphs()
VP = VisualizationPart(1280, 720, full_screen=False)

app = QApplication(sys.argv)
gui = MainWindow()

app.exec_()
