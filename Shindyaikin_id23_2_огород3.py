import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QGraphicsScene, QGraphicsView,
    QGraphicsPathItem, QVBoxLayout, QWidget, QPushButton, QSpinBox,
    QLabel, QHBoxLayout
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QColor, QPainterPath


class Cabbage:
    def __init__(self, volume, position):
        self.volume = volume
        self.position = position


class GoatHerd:
    def __init__(self, size, speed, endurance, eating_rate, fertility):
        self.size = size
        self.speed = speed
        self.endurance = endurance
        self.eating_rate = eating_rate
        self.fertility = fertility
        self.position = (250, 250)  # Starting position in the center of the garden


class GardenSimulation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Garden Simulation")
        self.setGeometry(100, 100, 800, 600)

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        self.cabbages = []
        self.goat_herds = []
        self.current_goat_herd = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(100)

        self.init_ui()
        self.draw_elements()

    def init_ui(self):
        control_panel = QWidget()
        layout = QVBoxLayout()

        # Controls for cabbage creation
        cabbage_layout = QHBoxLayout()
        self.cabbage_volume_input = QSpinBox()
        self.cabbage_volume_input.setRange(10, 200)
        cabbage_layout.addWidget(QLabel("Капуста (объем):"))
        cabbage_layout.addWidget(self.cabbage_volume_input)
        self.create_cabbage_button = QPushButton("Создать капусту")
        self.create_cabbage_button.clicked.connect(self.create_cabbage)
        cabbage_layout.addWidget(self.create_cabbage_button)
        layout.addLayout(cabbage_layout)

        # Controls for goat herd parameters
        herd_layout = QHBoxLayout()
        self.speed_input = QSpinBox()
        self.speed_input.setRange(1, 10)
        herd_layout.addWidget(QLabel("Скорость:"))
        herd_layout.addWidget(self.speed_input)

        self.eating_rate_input = QSpinBox()
        self.eating_rate_input.setRange(1, 20)
        herd_layout.addWidget(QLabel("Скорость поедания:"))
        herd_layout.addWidget(self.eating_rate_input)

        self.fertility_input = QSpinBox()
        self.fertility_input.setRange(1, 10)
        herd_layout.addWidget(QLabel("Плодовитость:"))
        herd_layout.addWidget(self.fertility_input)

        self.add_goat_herd_button = QPushButton("Добавить стадо")
        self.add_goat_herd_button.clicked.connect(self.add_goat_herd)
        herd_layout.addWidget(self.add_goat_herd_button)

        layout.addLayout(herd_layout)

        control_panel.setLayout(layout)
        control_panel.setFixedWidth(250)

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.view)
        self.main_layout.addWidget(control_panel)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # Enable clicking on the view to create cabbage
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
        size = 10  # Initial size
        speed = self.speed_input.value()
        endurance = 100  # Default value
        eating_rate = self.eating_rate_input.value()
        fertility = self.fertility_input.value()
        self.goat_herds.append(GoatHerd(size, speed, endurance, eating_rate, fertility))
        self.current_goat_herd = self.goat_herds[-1]  # Set the newly added herd as the current one
        self.draw_elements()

    def draw_elements(self):
        self.scene.clear()
        # Draw cabbages
        for cabbage in self.cabbages:
            x, y = cabbage.position
            size = cabbage.volume // 2  # Scale size for visualization
            self.scene.addEllipse(x - size, y - size, size * 2, size * 2, QColor(0, 255, 0), QColor(0, 255, 0, 150))

        # Draw goat herds
        for herd in self.goat_herds:
            x, y = herd.position
            size = herd.size * 2  # Scale size for visualization
            self.scene.addEllipse(x - size, y - size, size * 2, size * 2, QColor(255, 0, 0), QColor(255, 0, 0, 150))

    def update_simulation(self):
        # Simulate goat behavior for all herds
        for herd in self.goat_herds:
            if self.cabbages:
                closest_cabbage = min(self.cabbages, key=lambda c: self.distance(herd.position, c.position))
                distance_to_cabbage = self.distance(herd.position, closest_cabbage.position)

                if distance_to_cabbage < 20:  # Eating cabbage
                    herd.size += herd.fertility  # Increase herd size
                    closest_cabbage.volume -= herd.eating_rate
                    if closest_cabbage.volume <= 0:
                        self.cabbages.remove(closest_cabbage)
                else:
                    # Move towards cabbage
                    herd.position = (
                        herd.position[0] + (
                                    closest_cabbage.position[0] - herd.position[0]) / distance_to_cabbage * herd.speed,
                        herd.position[1] + (
                                    closest_cabbage.position[1] - herd.position[1]) / distance_to_cabbage * herd.speed,
                    )

        self.draw_elements()  # Redraw elements after updating positions

    @staticmethod
    def distance(pos1, pos2):
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


if __name__ == "__main__":
    app = QApplication(sys.argv)
    simulation = GardenSimulation()
    simulation.show()
    sys.exit(app.exec())
