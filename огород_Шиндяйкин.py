import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor


class Cabbage:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.eaten = False


class Goat:
    def __init__(self, x, y, size, speed, fertility, endurance):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.fertility = fertility
        self.endurance = endurance
        self.hunger = 0
        self.eating = False
        self.eating_progress = 0  # Progress of the eating animation

    def move_towards(self, cabbage):
        if cabbage:
            if self.x < cabbage.x:
                self.x += self.speed
            elif self.x > cabbage.x:
                self.x -= self.speed

            if self.y < cabbage.y:
                self.y += self.speed
            elif self.y > cabbage.y:
                self.y -= self.speed

    def eat(self, cabbage):
        if not cabbage.eaten:
            cabbage.eaten = True
            self.eating = True
            self.eating_progress = 0  # Reset eating progress
            self.size += self.fertility  # Increase goat size


class Herd:
    def __init__(self, goats):
        self.goats = goats

    def update(self, cabbages):
        for goat in self.goats:
            if goat.eating:
                if goat.eating_progress < 10:  # Simulate eating progress
                    goat.eating_progress += 1
                else:
                    goat.eating = False  # Finish eating

            else:
                if cabbages:
                    nearest_cabbage = min(
                        (c for c in cabbages if not c.eaten),
                        key=lambda c: (c.x - goat.x) ** 2 + (c.y - goat.y) ** 2,
                        default=None
                    )
                    goat.move_towards(nearest_cabbage)

                    if nearest_cabbage and abs(goat.x - nearest_cabbage.x) < 5 and abs(goat.y - nearest_cabbage.y) < 5:
                        goat.eat(nearest_cabbage)

            # Increase goat hunger
            goat.hunger += 0.4
            if goat.hunger > goat.endurance:
                goat.size = max(1, goat.size - 0.1)  # Decrease size due to hunger

    def spawn_new_cabbage(self, goat):
        # Create a new cabbage at a random location
        x = random.randint(50, 750)
        y = random.randint(50, 550)
        size = random.randint(10, 30)
        new_cabbage = Cabbage(x, y, size)
        return new_cabbage


class GardenSimulation(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Garden Simulation")
        self.setGeometry(100, 100, 800, 600)

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        self.cabbages = []
        self.herd = Herd([])

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(100)

        self.init_garden()

    def init_garden(self):
        # Create random cabbages
        for _ in range(10):
            x = random.randint(50, 750)
            y = random.randint(50, 550)
            size = random.randint(10, 30)
            cabbage = Cabbage(x, y, size)
            self.cabbages.append(cabbage)

        # Create goats
        for _ in range(1):
            x = random.randint(50, 750)
            y = random.randint(50, 550)
            size = random.randint(20, 40)
            goat = Goat(x, y, size, speed=5, fertility=2, endurance=10)
            self.herd.goats.append(goat)

    def update_simulation(self):
        self.herd.update(self.cabbages)
        self.scene.clear()  # Clear the scene for redrawing

        # Draw cabbages
        for cabbage in self.cabbages:
            if not cabbage.eaten:
                cabbage_item = QGraphicsEllipseItem(
                    cabbage.x - cabbage.size / 2,
                    cabbage.y - cabbage.size / 2,
                    cabbage.size,
                    cabbage.size
                )
                cabbage_item.setBrush(QColor(0, 255, 0))  # Green for cabbage
                self.scene.addItem(cabbage_item)

        # Draw goats
        for goat in self.herd.goats:
            if goat.eating:
                goat_arc_radius = goat.size / 2
                goat_arc_item = QGraphicsEllipseItem(
                    goat.x - goat_arc_radius,
                    goat.y - goat_arc_radius - goat.size,  # Position above the cabbage
                    goat.size,
                    goat.size
                )
                goat_arc_item.setBrush(QColor(165, 42, 42, 100))  # Semi-transparent brown
                goat_arc_item.setStartAngle(0 * 16)  # Start angle
                goat_arc_item.setSpanAngle(180 * 16)  # Half-circle
                self.scene.addItem(goat_arc_item)
            else:
                goat_item = QGraphicsEllipseItem(
                    goat.x - goat.size / 2,
                    goat.y - goat.size / 2,
                    goat.size,
                    goat.size
                )
                goat_item.setBrush(QColor(255, 255, 0))  # Yellow for goat
                self.scene.addItem(goat_item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    simulation = GardenSimulation()
    simulation.show()
    sys.exit(app.exec())
