#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
from random import random
import math

from PyQt6.QtCore import QTimer, Qt, QPointF
from PyQt6.QtGui import QPainter, QBrush, QColor, QPainterPath
from PyQt6.QtWidgets import QApplication, QWidget


class CircleAnimation(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Circle Animation")
        self.setGeometry(100, 100, 600, 600)
        self.radius = 200  # радиус окружности
        self.center_x = self.width() // 2
        self.center_y = self.height() // 2

        self.cabbages = [Cabbage(self.radius, [self.center_x, self.center_y]) for _ in range(5)]
        self.sheeps = [Sheep(self.radius, [self.center_x, self.center_y])]
        self.timer = QTimer(self)  # Таймер для обновления игры
        self.timer.timeout.connect(self.update_position)
        self.timer.start(16)

    def update_position(self):
        self.update()

    def add_cabbage(self):
        new_cabbage = Cabbage(self.radius, [self.center_x, self.center_y])

        # Проверка перекрытий с другими капустами
        while any(self.is_overlapping(new_cabbage, existing) for existing in self.cabbages):
            new_cabbage.generate_coords()  # Генерируем новые координаты, если есть перекрытие
        return new_cabbage

    def is_overlapping(self, cabbage1, cabbage2):
        distance = math.sqrt((cabbage1.x - cabbage2.x) ** 2 + (cabbage1.y - cabbage2.y) ** 2)
        return distance < cabbage1.size + cabbage2.size

    def get_purpose_cabbage(self):
        min_distance = float('inf')
        nearest_cabbage = None

        for cabbage in self.cabbages:
            for sheep in self.sheeps:
                distance = math.sqrt((cabbage.x - sheep.x) ** 2 + (cabbage.y - sheep.y) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    nearest_cabbage = cabbage

        return nearest_cabbage

    def paintEvent(self, event):
        painter = QPainter(self)

        # Рисуем окружность
        painter.setBrush(QBrush(Qt.GlobalColor.white, Qt.BrushStyle.SolidPattern))
        painter.drawEllipse(self.center_x - self.radius, self.center_y - self.radius, self.radius * 2, self.radius * 2)

        self.purpose_cabbage = self.get_purpose_cabbage()

        for cabbage in self.cabbages:
            # Рисуем капусту
            painter.setBrush(QBrush(QColor(0, 255, 0), Qt.BrushStyle.SolidPattern))
            painter.drawEllipse(int(cabbage.x - cabbage.size / 2), int(cabbage.y - cabbage.size / 2), int(cabbage.size),
                                int(cabbage.size))

            if cabbage.eaten_status:
                painter.setBrush(QBrush(Qt.GlobalColor.red, Qt.BrushStyle.SolidPattern))
                painter.drawEllipse(int(cabbage.x - cabbage.size / 2), int(cabbage.y - cabbage.size / 2),
                                    int(cabbage.size), int(cabbage.size))

        # Вычисляем расстояния и передвигаем овец
        self.sheeps_going()

        for sheep in self.sheeps:
            center = QPointF(sheep.x, sheep.y)
            painter.setBrush(QBrush(Qt.GlobalColor.lightGray, Qt.BrushStyle.SolidPattern))

            if not sheep.eating_status:
                painter.drawEllipse(center, sheep.size / 2, sheep.size / 2)

            if sheep.eating_status:
                path = QPainterPath()
                path.moveTo(sheep.x, sheep.y)
                path.arcTo(sheep.x - sheep.size / 2, sheep.y - sheep.size / 2,
                           sheep.size, sheep.size, 0, 180)

                painter.fillPath(path, painter.brush())
                painter.drawPath(path)

    def sheeps_going(self):
        distance_list = []
        for sheep in self.sheeps:
            if self.purpose_cabbage:  # Проверка на существование капусты
                dx = self.purpose_cabbage.x - sheep.x
                dy = self.purpose_cabbage.y - sheep.y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                distance_list.append(distance)
                sheep.move_towards(self.purpose_cabbage)

                # Проверка на поедание капусты
                if distance < sheep.size / 2 + self.purpose_cabbage.size / 2:
                    sheep.eating_status = True
                    self.purpose_cabbage.eaten_status = True
                    self.cabbages.remove(self.purpose_cabbage)  # Удаляем капусту после поедания
                else:
                    sheep.eating_status = False
                    if distance > self.purpose_cabbage.size - 2:
                        sheep.x += sheep.speed * (dx / distance)
                        sheep.y += sheep.speed * (dy / distance)
        return distance_list

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_E:
            self.cabbages.append(self.add_cabbage())
        if event.key() == Qt.Key.Key_Q:
            cords = [self.sheeps[-1].x, self.sheeps[-1].y]
            self.sheeps.append(Sheep(20, cords))


class Cabbage:
    def __init__(self, circle_radius, center):
        self.center = center
        self.circle_radius = circle_radius
        self.exist = False
        self.generate_coords()
        self.value = int((random() + 0.1) * 400)
        self.size = 2 * math.log(self.value)
        self.eaten_status = False

    def generate_coords(self):
        range = random() * (self.circle_radius * 0.95)
        angle = random() * 360
        self.x = self.center[0] + range * math.cos(math.radians(angle))
        self.y = self.center[1] + range * math.sin(math.radians(angle))
        self.value = int((random() + 0.1) * 400)


class Sheep:
    SHEEP_COUNT = 0

    def __init__(self, circle_radius, center):
        Sheep.SHEEP_COUNT += 1
        self.center = center
        self.circle_radius = circle_radius
        self.speed = 1  # Скорость передвижения
        self.hungry = (random() + 0.1) * 1000  # Голод
        self.reproduction_threshold = (random() + 0.1) * 2000  # Нужно еды для увеличения стада

        self.size = 15  # Размер овцы
        self.eating_status = False  # Статус поедания
        self.generate_coords()
        self.starve = 800
        self.eat_speed = self.change_eat_speed()

    def generate_coords(self):
        range_value = random() * (self.circle_radius * 0.95)
        angle = random() * 360
        self.x = self.center[0] + range_value * math.cos(math.radians(angle))
        self.y = self.center[1] + range_value * math.sin(math.radians(angle))

    def change_eat_speed(self):
        if self.starve > 700:
            return 10
        return (800 - self.starve) // 10

    def eat(self):
        if not self.eating_status:
            self.eating_status = True
            self.size += 5  # Увеличиваем размер после поедания

    def move_towards(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > target.size:  # Если не достигли капусты
            # Уменьшаем размер во время движения
            self.size -= 0.1
            if distance > target.size - 2:
                self.x += self.speed * (dx / distance)
                self.y += self.speed * (dy / distance)
        else:
            # Достигли капусты и едим
            self.eat()


# В методе sheeps_going нужно вызывать move_towards для каждого sheep.


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CircleAnimation()
    window.show()
    sys.exit(app.exec())


# In[ ]:




