import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QGraphicsScene, QGraphicsView,
    QVBoxLayout, QWidget, QPushButton, QSpinBox,
    QLabel, QHBoxLayout, QComboBox)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QColor, QPainterPath, QPen, QBrush


class Cabbage:
    def __init__(self, volume, position):
        self.volume = volume
        self.position = position
        self.is_being_eaten = False


class GoatHerd:
    def __init__(self, size, speed, endurance, eating_rate, fertility):
        self.size = size
        self.speed = speed
        self.endurance = endurance
        self.eating_rate = eating_rate
        self.fertility = fertility
        self.position = (250, 250)
        self.is_eating = False


class GardenSimulation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ОГОРОД")
        self.setGeometry(100, 100, 800, 600)
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)
        self.cabbages = []
        self.goat_herds = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(100)
        self.is_paused = False
        self.init_ui()
        self.draw_elements()

    def init_ui(self):
        control_panel = QWidget()
        layout = QVBoxLayout()
        cabbage_layout = QHBoxLayout()
        self.cabbage_volume_input = QSpinBox()
        self.cabbage_volume_input.setRange(10, 200)
        cabbage_layout.addWidget(QLabel("Капуста (объем):"))
        cabbage_layout.addWidget(self.cabbage_volume_input)
        self.create_cabbage_button = QPushButton("Создать капусту")
        self.create_cabbage_button.clicked.connect(self.create_cabbage)
        cabbage_layout.addWidget(self.create_cabbage_button)
        layout.addLayout(cabbage_layout)

        herd_layout = QHBoxLayout()
        self.speed_input = QSpinBox()
        self.speed_input.setRange(1, 10)
        herd_layout.addWidget(QLabel("Скорость:"))
        herd_layout.addWidget(self.speed_input)

        self.eating_rate_input = QSpinBox()
        self.eating_rate_input.setRange(1, 20)
        herd_layout.addWidget(QLabel("Скорость E:"))
        herd_layout.addWidget(self.eating_rate_input)

        self.fertility_input = QSpinBox()
        self.fertility_input.setRange(1, 10)
        herd_layout.addWidget(QLabel("Плодовитость:"))
        herd_layout.addWidget(self.fertility_input)

        self.add_goat_herd_button = QPushButton("Добавить стадо")
        self.add_goat_herd_button.clicked.connect(self.add_goat_herd)
        herd_layout.addWidget(self.add_goat_herd_button)
        layout.addLayout(herd_layout)

        self.herd_selector = QComboBox()
        self.herd_selector.currentIndexChanged.connect(self.select_goat_herd)
        layout.addWidget(QLabel("Выберите стадо:"))
        layout.addWidget(self.herd_selector)

        self.update_herd_button = QPushButton("Обновить параметры стада")
        self.update_herd_button.clicked.connect(self.update_goat_herd_parameters)
        layout.addWidget(self.update_herd_button)

        self.pause_button = QPushButton("Пауза")
        self.pause_button.clicked.connect(self.pause_animation)
        layout.addWidget(self.pause_button)

        self.resume_button = QPushButton("Возобновить")
        self.resume_button.clicked.connect(self.resume_animation)
        layout.addWidget(self.resume_button)

        control_panel.setLayout(layout)
        control_panel.setFixedWidth(350)

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.view)
        self.main_layout.addWidget(control_panel)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        self.view.setMouseTracking(True)
        self.view.mousePressEvent = self.create_cabbage_on_click

    def create_cabbage_on_click(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            volume = self.cabbage_volume_input.value()
            position = (event.position().x(), event.position().y())
            self.cabbages.append(Cabbage(volume, position))
            self.draw_elements()

    def create_cabbage(self):
        volume = self.cabbage_volume_input.value()
        position = (random.randint(50, 450), random.randint(50, 450))
        self.cabbages.append(Cabbage(volume, position))
        self.draw_elements()

    def add_goat_herd(self):
        size = 10
        speed = self.speed_input.value()
        endurance = 100
        eating_rate = self.eating_rate_input.value()
        fertility = self.fertility_input.value()
        herd = GoatHerd(size, speed, endurance, eating_rate, fertility)
        self.goat_herds.append(herd)
        self.herd_selector.addItem(f"Стадо {len(self.goat_herds)}")
        self.draw_elements()

    def select_goat_herd(self, index):
        if index >= 0 and index < len(self.goat_herds):
            selected_herd = self.goat_herds[index]
            self.speed_input.setValue(selected_herd.speed)
            self.eating_rate_input.setValue(selected_herd.eating_rate)
            self.fertility_input.setValue(selected_herd.fertility)

    def update_goat_herd_parameters(self):
        index = self.herd_selector.currentIndex()
        if index >= 0 and index < len(self.goat_herds):
            selected_herd = self.goat_herds[index]
            selected_herd.speed = self.speed_input.value()
            selected_herd.eating_rate = self.eating_rate_input.value()
            selected_herd.fertility = self.fertility_input.value()
            self.draw_elements()

    def draw_elements(self):
        self.scene.clear()

        for cabbage in self.cabbages:
            x, y = cabbage.position
            size = cabbage.volume // 2
            path = QPainterPath()

            if cabbage.is_being_eaten:
                path.moveTo(x, y)
                path.arcTo(x - size, y - size, size * 2, size * 2, 0, -180)
                self.scene.addPath(path, QPen(QColor(0, 255, 0)), QBrush(QColor(0, 255, 0)))
            else:
                self.scene.addEllipse(x - size, y - size, size * 2, size * 2, QPen(QColor(0, 255, 0)),
                                      QBrush(QColor(0, 255, 0)))

        for herd in self.goat_herds:
            x, y = herd.position
            size = herd.size

            path = QPainterPath()
            if herd.is_eating:
                path.moveTo(x, y)
                path.arcTo(x - size, y - size, size * 2, size * 2, 0, 180)
                self.scene.addPath(path, QPen(QColor(255, 0, 0)), QBrush(QColor(255, 0, 0)))
            else:
                self.scene.addEllipse(x - size, y - size, size * 2, size * 2, QPen(QColor(255, 0, 0)),
                                      QBrush(QColor(255, 0, 0)))

    def pause_animation(self):
        self.is_paused = True
        self.timer.stop()

    def resume_animation(self):
        if self.is_paused:
            self.is_paused = False
            self.timer.start(100)

    def update_simulation(self):
        if not self.is_paused:
            for herd in self.goat_herds[:]:
                if self.cabbages:
                    closest_cabbage = min(self.cabbages, key=lambda c: self.distance(herd.position, c.position))
                    distance_to_cabbage = self.distance(herd.position, closest_cabbage.position)

                    if distance_to_cabbage < 10:
                        herd.is_eating = True
                        closest_cabbage.is_being_eaten = True
                        herd.size += closest_cabbage.volume * 0.1
                        closest_cabbage.volume -= herd.eating_rate

                        if closest_cabbage.volume <= 0:
                            self.cabbages.remove(closest_cabbage)
                    else:
                        herd.is_eating = False
                        closest_cabbage.is_being_eaten = False
                        herd.size -= 0.1
                        herd.position = (
                            herd.position[0] + (closest_cabbage.position[0] - herd.position[
                                0]) / distance_to_cabbage * herd.speed,
                            herd.position[1] + (closest_cabbage.position[1] - herd.position[
                                1]) / distance_to_cabbage * herd.speed,
                        )

                    if herd.size <= 0:
                        self.goat_herds.remove(herd)

        self.draw_elements()

    @staticmethod
    def distance(pos1, pos2):
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


if __name__ == "__main__":
    app = QApplication(sys.argv)
    simulation = GardenSimulation()
    simulation.show()
    sys.exit(app.exec())
