import sys
from PyQt6 import QtWidgets, QtCore, QtGui


class BalloonSimulation(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Симуляция запуска воздушного шара")
        self.setGeometry(100, 100, 800, 600)

        # Элементы управления
        self.volume_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.volume_slider.setRange(1, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.volume_slider.setTickInterval(10)

        self.mass_spinbox = QtWidgets.QSpinBox()
        self.mass_spinbox.setRange(0, 100)
        self.mass_spinbox.setValue(10)

        self.speed_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.speed_slider.setRange(1, 100)
        self.speed_slider.setValue(50)
        self.speed_slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.speed_slider.setTickInterval(10)

        self.start_button = QtWidgets.QPushButton("Запустить")
        self.reset_button = QtWidgets.QPushButton("Сбросить")

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Объем шара:"))
        layout.addWidget(self.volume_slider)
        layout.addWidget(QtWidgets.QLabel("Масса груза:"))
        layout.addWidget(self.mass_spinbox)
        layout.addWidget(QtWidgets.QLabel("Скорость подъема:"))
        layout.addWidget(self.speed_slider)
        layout.addWidget(self.start_button)
        layout.addWidget(self.reset_button)

        self.setLayout(layout)

        # Подключение сигналов
        self.start_button.clicked.connect(self.start_animation)
        self.reset_button.clicked.connect(self.reset_balloon)

        # Анимация
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_position)
        self.is_moving = False
        self.current_height = 500
        self.v0 = 0  # Начальная скорость

    def start_animation(self):
        if not self.is_moving:
            self.is_moving = True
            self.v0 = self.speed_slider.value()  # Устанавливаем начальную скорость
            self.timer.start(50)  # Обновление каждые 50 мс

    def reset_balloon(self):
        self.is_moving = False
        self.current_height = 500
        self.v0 = 0
        self.timer.stop()
        self.update()

    def update_position(self):
        V = self.volume_slider.value()
        m = self.mass_spinbox.value()
        ρair = 1.225  # Плотность воздуха
        g = 9.81  # Ускорение свободного падения в м/с
        Flift = V * ρair * g
        Fgravity = m * g

        # Ускорение
        a = (Flift - Fgravity) / m if m > 0 else 0

        # Обновление высоты и скорости
        self.current_height -= self.v0 * 0.05 + (
                ((0.05 ** 2) * (Flift - Fgravity)) / 2 * m)  # Высота уменьшается, так как y вниз
        self.v0 += a * 0.05

        # Проверка на достижение верхней границы окна
        if self.current_height < 0:
            self.current_height = 0
            self.is_moving = False
            self.timer.stop()

        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setBrush(QtGui.QColor(255, 0, 0, 150))
        painter.drawEllipse(350, int(self.current_height), 50, 50)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = BalloonSimulation()
    window.show()
    sys.exit(app.exec())
