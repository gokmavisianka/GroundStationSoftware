from PySide2.Qt3DExtras import Qt3DExtras
from PySide2.Qt3DCore import Qt3DCore
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import pygame
import math


clock = pygame.time.Clock()


class V3D(QWidget):
    def __init__(self, root_entity=None):
        super().__init__()

        self.cuboids = {}
        self.texts = {}

        self.parent = None

        self.m_rootEntity = root_entity

        self.x = self.y = self.z = 0

        self.create_cuboid(name="rocket", scale3D=QVector3D(0.8, 8.0, 0.8), color="gray")
        self.create_cuboid(name="x_axis", scale3D=QVector3D(6.0, 0.1, 0.1), translation=QVector3D(3.0, 0.0, 0.0), color="red")
        self.create_cuboid(name="y_axis", scale3D=QVector3D(0.1, 6.0, 0.1), translation=QVector3D(0.0, 3.0, 0.0), color="green")
        self.create_cuboid(name="z_axis", scale3D=QVector3D(0.1, 0.1, 6.0), translation=QVector3D(0.0, 0.0, 3.0), color="blue")

        self.start()

        self.create_text(code="x", text="x", color="red", translation=QVector3D(5.25, 0.0, 0.0), root=self.m_rootEntity)
        self.create_text(code="y", text="y", color="green", translation=QVector3D(0.4, 4.9, 0.0), rotation={"x": 0, "y": 45, "z": 0}, root=self.m_rootEntity)
        self.create_text(code="z", text="z", color="blue", translation=QVector3D(0.0, 0.0, 5.75), rotation={"x": 0, "y": 90, "z": 0}, root=self.m_rootEntity)

        # self.create_text(code="pitch", text="pitch: ", color="red", translation=QVector3D(-5, 3.9, 3), rotation={"x": 0, "y": 45, "z": 0}, root=self.m_rootEntity)
        # self.create_text(code="roll", text="roll: ", color="green", translation=QVector3D(-5, 2.9, 3), rotation={"x": 0, "y": 45, "z": 0}, root=self.m_rootEntity)
        # self.create_text(code="yaw", text="yaw: ", color="blue", translation=QVector3D(-5, 2.9, 3), rotation={"x": 0, "y": 45, "z": 0}, root=self.m_rootEntity)

    def additional_setup(self, name, geometry, minimum_size, maximum_size, group_box_style, parent, texts):
        x, y, width, height = geometry
        self.items = {}
        self.TextObjects = {}
        self.text_properties = texts
        
        self.group_box = QGroupBox(parent)
        self.group_box.setMinimumSize(minimum_size)
        self.group_box.setMaximumSize(maximum_size)
        self.group_box.setGeometry(QRect(x, y, width, height))
        self.group_box.setStyleSheet(group_box_style)
        self.group_box.show()

        self.setup_texts(texts)
        
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
        self.TextObjects[key].setText(f"{self.text_properties[key]['value']}: {value}")
    
    def show_name(self, name):
        self.create_text(code=name, text=name, color="yellow", translation=QVector3D(3, 3.9, -5), rotation={"x": 0, "y": 45, "z": 0}, root=self.m_rootEntity)

    def create_text(self, code, text, root=None, color="white", height=20, width=100, scale=0.075, translation=QVector3D(0.0, 0.0, 0.0), rotation={"x": 0, "y": 0, "z": 0}):
        self.textTransform = Qt3DCore.QTransform(scale=scale, translation=translation)
        self.textTransform.setRotationX(rotation["x"])
        self.textTransform.setRotationY(rotation["y"])
        self.textTransform.setRotationZ(rotation["z"])
        self.text = Qt3DExtras.QText2DEntity(root)
        self.text.setFont("monospace")
        self.text.setHeight(height)
        self.text.setWidth(width)
        self.text.setText(text)
        self.text.setColor(QColor(color))
        self.text.addComponent(self.textTransform)

        self.texts.update({code: {"text": self.text, "transform": self.textTransform}})

    def create_cuboid(self, name, scale3D=QVector3D(1.0, 1.0, 1.0), translation=QVector3D(0.0, 0.0, 0.0), color="white"):
        self.cuboids.update({name: {"model": Qt3DExtras.QCuboidMesh(),
                                    "transform": Qt3DCore.QTransform(scale3D=scale3D, translation=translation),
                                    "material": Qt3DExtras.QPhongMaterial(diffuse=QColor(color)),
                                    "entity": Qt3DCore.QEntity(self.m_rootEntity)}})

        for key in ["model", "transform", "material"]:
            self.cuboids[name]["entity"].addComponent(self.cuboids[name][key])

    def rotate_around_x(self, cuboid, rotation_x=30):
        transform = self.cuboids[cuboid]["transform"]
        if rotation_x != 0:
            coefficient = transform.scale3D().y() / 2
            y = round(coefficient * math.cos(math.radians(rotation_x)), 4)
            z = round(coefficient * math.sin(math.radians(rotation_x)), 4)
            transform.setRotationX(rotation_x)
            transform.setTranslation(QVector3D(0.0, y, z))

    def rotate_around_y(self, cuboid, rotation_y=60):
        transform = self.cuboids[cuboid]["transform"]
        if rotation_y != 0:
            coefficient = transform.scale3D().z() / 2
            x = round(coefficient * math.sin(math.radians(rotation_y)), 4)
            z = round(coefficient * math.cos(math.radians(rotation_y)), 4)
            transform.setRotationY(rotation_y)
            transform.setTranslation(QVector3D(x, 0.0, z))

    def rotate_around_z(self, cuboid, rotation_z=45):
        transform = self.cuboids[cuboid]["transform"]
        if rotation_z != 0:
            coefficient = transform.scale3D().y() / 2
            x = round(coefficient * math.sin(math.radians(rotation_z)), 4)
            y = round(coefficient * math.cos(math.radians(rotation_z)), 4)
            transform.setRotationZ(rotation_z)
            transform.setTranslation(QVector3D(-x, y, 0.0))

    def update_rotation(self, data):
        self.x = data["x"]
        self.y = data["y"]
        self.z = data["z"]

    def start(self):
        self.thread = QThread()
        self.worker = Worker(master=self, prnt=self)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()


class Worker(QObject):
    def __init__(self, master, prnt):
        super().__init__()
        self.parent = prnt
        self.master = master

    def run(self, rotations_per_second=10):
        modifier = self.master
        while True:
            try:
                self.parent.update_text("roll", self.parent.x)
                self.parent.update_text("pitch", self.parent.y)
                self.parent.update_text("yaw", self.parent.z)
            except AttributeError:
                print("Attribute Error: ")
                print("Text Objects for ('roll', 'pitch' and 'yaw') are still not created!\n")
            modifier.cuboids["rocket"]["transform"].setRotationX(self.parent.x)
            modifier.cuboids["rocket"]["transform"].setRotationY(self.parent.z)
            modifier.cuboids["rocket"]["transform"].setRotationZ(self.parent.y)
            clock.tick(rotations_per_second)
