from PySide2.Qt3DExtras import Qt3DExtras
from PySide2.Qt3DRender import Qt3DRender
from PySide2.Qt3DCore import Qt3DCore
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from source_ConditionLabel import ConditionLabel
from source_SerialPort import SerialPort
from source_LineGraph import LineGraph
from source_BarGraph import BarGraph
from source_V3D import V3D
from pygame import time
from random import randint
import sys

clock = time.Clock()

ConditionLabels = {}
LineGraphs = {}
BarGraphs = {}
elements = {}
V3Ds = {}

def initiate(parent):
    ConditionLabels["0"] = ConditionLabel(base_text="İlk Kurtarma",
                                          geometry=(1590, 30, 300, 58),
                                          minimum_size=QSize(300, 60),
                                          maximum_size=QSize(300, 60),
                                          font={"color": "black", "size": 16},
                                          data={"texts": {False: "Gerçekleşmedi", True: "Gerçekleşti"},
                                                "colors": {False: "red", True: "lime"},
                                                "border_color": {False: "rgb(200, 0, 0)", True: "rgb(0, 200, 0)"}},
                                          border={"width": 4},
                                          initial_value=False,
                                          parent=parent)

    ConditionLabels["1"] = ConditionLabel(base_text="İkinci Kurtarma",
                                          geometry=(1590, 118, 300, 57),
                                          minimum_size=QSize(300, 60),
                                          maximum_size=QSize(300, 60),
                                          font={"color": "black", "size": 15},
                                          data={"texts": {False: "Gerçekleşmedi", True: "Gerçekleşti"},
                                                "colors": {False: "red", True: "lime"},
                                                "border_color": {False: "rgb(200, 0, 0)", True: "rgb(0, 200, 0)"}},
                                          border={"width": 4},
                                          initial_value=False,
                                          parent=parent)

    ConditionLabels["2"] = ConditionLabel(base_text="Etkin Sistem",
                                          geometry=(1590, 205, 300, 57),
                                          minimum_size=QSize(300, 60),
                                          maximum_size=QSize(300, 60),
                                          font={"color": "black", "size": 16},
                                          data={"texts": {False: "Ana Aviyonik", True: "Yedek Aviyonik"},
                                                "colors": {False: "red", True: "lime"},
                                                "border_color": {False: "rgb(200, 0, 0)", True: "rgb(0, 200, 0)"}},
                                          border={"width": 4},
                                          initial_value=False,
                                          parent=parent)

    ConditionLabels["3"] = ConditionLabel(base_text="Faydalı Yük",
                                          geometry=(1590, 292, 300, 58),
                                          minimum_size=QSize(300, 60),
                                          maximum_size=QSize(300, 60),
                                          font={"color": "black", "size": 16},
                                          data={"texts": {False: "Veri Alınamıyor", True: "Veri Alınıyor"},
                                                "colors": {False: "red", True: "lime"},
                                                "border_color": {False: "rgb(200, 0, 0)", True: "rgb(0, 200, 0)"}},
                                          border={"width": 4},
                                          initial_value=False,
                                          parent=parent)

    LineGraphs["temperature"] = LineGraph(parent=parent,
                                          grids={"x": True, "y": True},
                                          geometry=(30, 30, 490, 270),
                                          minimum_size=QSize(490, 320),
                                          maximum_size=QSize(490, 320),
                                          background_color="white",
                                          group_box_style="border: 1px solid green;",
                                          texts={"rocket": {"value": 'Roket', "font": {"size": 16, "color": "purple"}, "geometry": (10, 260, 235, 50)},
                                                 "payload": {"value": 'Faydalı Yük', "font": {"size": 16, "color": "pink"}, "geometry": (245, 260, 235, 50)}},
                                          styles={"color": 'orange', "font-size": '20px'},
                                          colors=["red", "blue"],
                                          labels={"x": {"position": "bottom", "text": "Zaman", "unit": "s"},
                                                  "y": {"position": "left", "text": "Sıcaklık", "unit": "°C"},
                                                  "0": {"position": "right", "text": " ", "unit": ""},
                                                  "1": {"position": "top", "text": " ", "unit": ""}},
                                          variables={"rocket": {"values": [],
                                                               "pen": {"color": "purple", "width": 2},
                                                               "symbol": {"key": "o", "size": 16, "color": "purple"}},
                                                     "payload": {"values": [],
                                                                     "pen": {"color": "pink", "width": 2},
                                                                     "symbol": {"key": "o", "size": 16, "color": "pink"}}})

    LineGraphs["pressure"] = LineGraph(parent=parent,
                                       grids={"x": True, "y": True},
                                       geometry=(550, 30, 490, 270),
                                       minimum_size=QSize(490, 320),
                                       maximum_size=QSize(490, 320),
                                       background_color="white",
                                       group_box_style="border: 1px solid green;",
                                       texts={"rocket": {"value": 'Roket', "font": {"size": 16, "color": "purple"}, "geometry": (10, 260, 235, 50)},
                                              "payload": {"value": 'Faydalı Yük', "font": {"size": 16, "color": "pink"}, "geometry": (245, 260, 235, 50)}},
                                       styles={"color": 'orange', "font-size": '20px'},
                                       colors=["red", "blue"],
                                       labels={"x": {"position": "bottom", "text": "Zaman", "unit": "s"},
                                               "y": {"position": "left", "text": "Basınç", "unit": "Pa"},
                                               "0": {"position": "right", "text": " ", "unit": ""},
                                               "1": {"position": "top", "text": " ", "unit": ""}},
                                       variables={"rocket": {"values": [],
                                                            "pen": {"color": "purple", "width": 2},
                                                            "symbol": {"key": "o", "size": 16, "color": "purple"}},
                                                  "payload": {"values": [],
                                                                  "pen": {"color": "pink", "width": 2},
                                                                  "symbol": {"key": "o", "size": 16, "color": "pink"}}})

    LineGraphs["altitude"] = LineGraph(parent=parent,
                                     grids={"x": True, "y": True},
                                     geometry=(1070, 30, 490, 270),
                                     minimum_size=QSize(490, 320),
                                     maximum_size=QSize(490, 320),
                                     background_color="white",
                                     group_box_style="border: 1px solid green;",
                                     texts={"rocket": {"value": 'Roket', "font": {"size": 16, "color": "purple"}, "geometry": (10, 260, 235, 50)},
                                            "payload": {"value": 'Faydalı Yük', "font": {"size": 16, "color": "pink"}, "geometry": (245, 260, 235, 50)}},
                                     styles={"color": 'orange', "font-size": '20px'},
                                     colors=["red", "blue"],
                                     labels={"x": {"position": "bottom", "text": "Zaman", "unit": "s"},
                                             "y": {"position": "left", "text": "İrtifa", "unit": "m"},
                                             "0": {"position": "right", "text": " ", "unit": ""},
                                             "1": {"position": "top", "text": " ", "unit": ""}},
                                     variables={"rocket": {"values": [],
                                                          "pen": {"color": "purple", "width": 2},
                                                          "symbol": {"key": "o", "size": 16, "color": "purple"}},
                                                "payload": {"values": [],
                                                                "pen": {"color": "pink", "width": 2},
                                                                "symbol": {"key": "o", "size": 16, "color": "pink"}}})

    BarGraphs["rocket"] = BarGraph(name="RocketAcceleration",
                                   geometry=(30, 730, 490, 270),
                                   width=0.5,
                                   brush="green",
                                   grids={"x": True, "y": True},
                                   variables={"x": 0, "y": 0, "z": 0},
                                   colors=["red", "green", "blue"],
                                   background_color="white",
                                   parent=parent,
                                   group_box_style=("border: 1px solid green;"),
                                   texts={"x": {"value": 'x', "font": {"size": 16, "color": "red"},
                                                "geometry": (10, 260, 157, 50)},
                                          "y": {"value": 'y', "font": {"size": 16, "color": "green"},
                                                "geometry": (167, 260, 156, 50)},
                                          "z": {"value": 'z', "font": {"size": 16, "color": "blue"},
                                                "geometry": (323, 260, 157, 50)}},
                                   minimum_size=QSize(490, 320),
                                   maximum_size=QSize(490, 320),
                                   styles={"color": 'orange', "font-size": '20px'},
                                   labels={"title": {"position": "top", "text": "(Roket)", "unit": ""},
                                           "y": {"position": "left", "text": "ivme", "unit": "m/s²"},
                                           "_": {"position": "right", "text": " ", "unit": ""}})

    BarGraphs["payload"] = BarGraph(name="PayloadAcceleration",
                                    geometry=(550, 730, 490, 270),
                                    width=0.5,
                                    brush="green",
                                    grids={"x": True, "y": True},
                                    variables={"x": 0, "y": 0, "z": 0},
                                    colors=["red", "green", "blue"],
                                    background_color="white",
                                    parent=parent,
                                    group_box_style=("border: 1px solid green;"),
                                    texts={"x": {"value": 'x', "font": {"size": 16, "color": "red"},
                                                 "geometry": (10, 260, 157, 50)},
                                           "y": {"value": 'y', "font": {"size": 16, "color": "green"},
                                                 "geometry": (167, 260, 156, 50)},
                                           "z": {"value": 'z', "font": {"size": 16, "color": "blue"},
                                                 "geometry": (323, 260, 157, 50)}},
                                    minimum_size=QSize(490, 320),
                                    maximum_size=QSize(490, 320),
                                    styles={"color": 'orange', "font-size": '20px'},
                                    labels={"title": {"position": "top", "text": "(Faydalı Yük)", "unit": ""},
                                            "y": {"position": "left", "text": "ivme", "unit": "m/s²"},
                                            "_": {"position": "right", "text": " ", "unit": ""}})

    create_V3D("rocket")
    create_V3D("payload")
    Layout = QGridLayout(parent)
    Layout.setContentsMargins(0, 380, 1920-1070, 380)
    Layout.setSpacing(0)
    Layout.addWidget(V3Ds["rocket"]["container"], 0, 0)
    Layout.addWidget(V3Ds["payload"]["container"], 0, 1)

    container_box_rocket = QGroupBox(parent)
    container_box_rocket.setGeometry(QRect(30, 380, 490, 320))
    container_box_rocket.setStyleSheet("border: 1px solid lime;")
    container_box_rocket.show()
    container_box_payload = QGroupBox(parent)
    container_box_payload.setGeometry(QRect(550, 380, 490, 320))
    container_box_payload.setStyleSheet("border: 1px solid lime;")
    container_box_payload.show()

    elements["SerialPort"] = SerialPort(parent=parent,
                                        geometry=(1070, 380, 820, 670),
                                        font={"color": 'black', "size": 16},
                                        background_color="white",
                                        border={"width": 2, "color": 'rgb(170, 80, 0)'},
                                        ConditionLabels=ConditionLabels,
                                        LineGraphs=LineGraphs,
                                        BarGraphs=BarGraphs,
                                        V3Ds=V3Ds)

    elements["ConditionLabel"] = ConditionLabel(base_text="Durum",
                                                geometry=(560, 600, 250, 60),
                                                minimum_size=QSize(250, 60),
                                                maximum_size=QSize(250, 60),
                                                font={"color": "black", "size": 16},
                                                data={"texts": {False: "Bağlantı Yok", True: "Bağlantı Kuruldu"},
                                                      "colors": {False: "red", True: "lime"},
                                                      "border_color": {False: "rgb(200, 0, 0)",
                                                                       True: "rgb(0, 200, 0)"}},
                                                border={"width": 4},
                                                initial_value=False,
                                                parent=elements["SerialPort"].group_box)

    elements["SerialPort"].labels["condition"] = elements["ConditionLabel"]

    for name in ("rocket", "payload"):
        if name == "rocket":
            x = 30
        elif name == "payload":
            x = 550
        V3Ds[name]["modifier"].additional_setup(name=f"V3D_{name}_angles",
                                                parent=parent,
                                                geometry=(x, 380, 1920-1070, 380),
                                                minimum_size=QSize(490, 320),
                                                maximum_size=QSize(490, 320),
                                                group_box_style=("border: 1px solid lime;"),
                                                texts={"roll": {"value": 'roll', "font": {"size": 16, "color": "red"},
                                                                "geometry": (10, 290, 157, 30)},
                                                       "pitch": {"value": 'pitch', "font": {"size": 16, "color": "green"},
                                                                 "geometry": (167, 290, 156, 30)},
                                                       "yaw": {"value": 'yaw', "font": {"size": 16, "color": "blue"},
                                                               "geometry": (323, 290, 157, 30)}})

    
                                                
def create_V3D(name, background_color="black", minimum_size=QSize(490, 270), maximum_size=QSize(490, 270)):
    def create_camera(view):
        cameraEntity = view.camera()
        cameraEntity.lens().setPerspectiveProjection(45.0, 16.0 / 9.0, 0.1, 1000.0)
        cameraEntity.setPosition(QVector3D(0, 5.0, 15.0))
        cameraEntity.setUpVector(QVector3D(0, 1, 0))
        cameraEntity.setViewCenter(QVector3D(0, 0, 0))
        cameraEntity.rotateAboutViewCenter(QQuaternion(0.923880, 0.000000, 0.382683, 0.000000))
        return cameraEntity

    def create_light(root, camera, intensity=1, color="white"):
        lightEntity = Qt3DCore.QEntity(root)
        lightObject = Qt3DRender.QPointLight(lightEntity)
        lightObject.setColor(color)
        lightObject.setIntensity(intensity)
        lightEntity.addComponent(lightObject)
        lightTransform = Qt3DCore.QTransform(lightEntity)
        lightTransform.setTranslation(camera.position())
        lightEntity.addComponent(lightTransform)
        return {"lightEntity": lightEntity, "lightObject": lightObject, "lightTransform": lightTransform}

    def create_view(background_color="black"):
        view = Qt3DExtras.Qt3DWindow()
        view.defaultFrameGraph().setClearColor(QColor(background_color))
        return view

    def create_container(view, minimum_size=QSize(470, 270), maximum_size=QSize(470, 270)):
        container = QWidget.createWindowContainer(view)
        container.setMinimumSize(minimum_size)
        container.setMaximumSize(maximum_size)
        return container

    def create_root():
        rootEntity = Qt3DCore.QEntity()
        return rootEntity

    def create_modifier(view, Class, root):
        modifier = Class(root)
        view.setRootEntity(root)
        return modifier

    view = create_view(background_color=background_color)
    container = create_container(view=view, minimum_size=minimum_size, maximum_size=maximum_size)
    root = create_root()
    camera = create_camera(view=view)
    light = create_light(root=root, camera=camera)
    modifier = create_modifier(view=view, Class=V3D, root=root)

    V3Ds.update({name: {"view": view,
                        "container": container,
                        "root": root,
                        "camera": camera,
                        "light": light,
                        "modifier": modifier}})


# Step 1: Create a worker class
class Worker(QObject):
    timer=QTimer()
        
    def run(self, outputs_per_second=1):
        while True:
            process()
            clock.tick(outputs_per_second)

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.setFixedSize(1920, 1080)
        self.showFullScreen()
        self.setup_all()
        self.show()

    def setup_all(self):
        initiate(self)
        V3Ds["rocket"]["modifier"].show_name("Roket")
        V3Ds["payload"]["modifier"].show_name("Faydalı Yük")
        self.runLongTask()

    def runLongTask(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.thread.deleteLater)
        # Step 6: Start the thread
        self.thread.start()
        

def process():
    elements["SerialPort"].project()
    liste = [randint(-50, 50) for number in range(18)]
    elements["SerialPort"].to_write = [":".join(str(element) for element in liste)]
    d1 = {"rocket": liste[0], "payload": liste[1]}
    d2 = {"rocket": liste[2], "payload": liste[3]}
    d3 = {"rocket": liste[4], "payload": liste[5]}
    d4 = {"x": liste[6], "y": liste[7], "z": liste[8]}
    d5 = {"x": liste[9], "y": liste[10], "z": liste[11]}
    d6 = {"x": liste[12], "y": liste[13], "z": liste[14]}
    d7 = {"x": liste[15], "y": liste[16], "z": liste[17]}
    LineGraphs["temperature"].append_to_data(d1)
    LineGraphs["pressure"].append_to_data(d2)
    LineGraphs["altitude"].append_to_data(d3)
    BarGraphs["rocket"].update_bar_graph_items(d4)
    BarGraphs["payload"].update_bar_graph_items(d5)
    V3Ds["rocket"]["modifier"].update_rotation(d6)
    V3Ds["payload"]["modifier"].update_rotation(d7)
    LineGraphs["temperature"].update_graph()
    LineGraphs["pressure"].update_graph()
    LineGraphs["altitude"].update_graph()

app = QApplication(sys.argv)

widget = MainWindow()
widget.show()

app.exec_()
