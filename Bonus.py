#Chat GPT assited 
import sys
import numpy as np
import math
from scipy.integrate import odeint
from scipy.optimize import minimize
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

class Spring(qtw.QGraphicsItem):
    def __init__(self, x, y, length, coils, pen=None, parent=None):
        super().__init__(parent)
        self.x = x
        self.y = y
        self.length = length
        self.coils = coils
        self.pen = pen

    def boundingRect(self):
        return qtc.QRectF(self.x, self.y - 10, self.length, 20)

    def paint(self, painter, option, widget=None):
        path = qtg.QPainterPath()
        path.moveTo(self.x, self.y)
        for i in range(1, self.coils + 1):
            # Alternating heights for the spring coils
            height = 20 if i % 2 == 0 else -20
            path.lineTo(self.x + i * self.length / self.coils, self.y + height)
        path.lineTo(self.x + self.length, self.y)
        if self.pen:
            painter.setPen(self.pen)
        painter.drawPath(path)

class Damper(qtw.QGraphicsItem):
    def __init__(self, x, y, length, pen=None, parent=None):
        super().__init__(parent)
        self.x = x
        self.y = y
        self.length = length
        self.pen = pen

    def boundingRect(self):
        return qtc.QRectF(self.x, self.y - 5, self.length, 10)

    def paint(self, painter, option, widget=None):
        if self.pen:
            painter.setPen(self.pen)
        # Drawing the damper line and the ends
        painter.drawLine(self.x, self.y, self.x + self.length, self.y)
        painter.drawLine(self.x, self.y - 5, self.x, self.y + 5)
        painter.drawLine(self.x + self.length, self.y - 5, self.x + self.length, self.y + 5)

class CarModel:
    def __init__(self):
        self.tmax = 3.0
        self.t = np.linspace(0, self.tmax, 200)
        self.tramp = 1.0
        self.angrad = 0.1
        self.ymag = 6.0 / (12 * 3.3)
        self.yangdeg = 45.0
        self.results = None

        # Car properties
        self.m1 = 450
        self.m2 = 20
        self.c1 = 4500
        self.k1 = 15000
        self.k2 = 90000
        self.v = 120

        # Limits
        self.mink1 = 43449.8
        self.maxk1 = 86899.6
        self.mink2 = 3862.2
        self.maxk2 = 7724.4
        self.accelMax = 19.62
        self.accelLim = 19.62
        self.SSE = 0.0

class CarView(qtw.QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.setupUI()

    def setupUI(self):
        # Main layout
        self.layout = qtw.QVBoxLayout()
        self.setLayout(self.layout)

        # Graphics View for schematic
        self.scene = qtw.QGraphicsScene()
        self.gv_Schematic = qtw.QGraphicsView(self.scene)
        self.layout.addWidget(self.gv_Schematic)

        # Setup scene
        self.setupPensAndBrushes()
        self.buildScene()

    def setupPensAndBrushes(self):
        self.penWheel = qtg.QPen(qtg.QColor("orange"), 1)
        self.brushWheel = qtg.QBrush(qtg.QColor.fromHsv(35, 255, 255, 64))
        self.brushMass = qtg.QBrush(qtg.QColor(200, 200, 200, 128))

    def buildScene(self):
        self.scene.setSceneRect(-200, -200, 400, 400)
        # Add custom spring and damper
        spring = Spring(0, -50, 100, 10, self.penWheel)
        damper = Damper(0, -100, 100, self.penWheel)
        self.scene.addItem(spring)
        self.scene.addItem(damper)

def main():
    app = qtw.QApplication(sys.argv)
    model = CarModel()
    view = CarView(model)
    view.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
