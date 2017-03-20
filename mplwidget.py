#! encoding:utf8 #

import numpy as np

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget

# Matplolib figure object
from matplotlib.figure import Figure

# import the Qt5Agg FigureCanvas object, that binds Figure to Qt5Agg
# backend. It also inherits from QWidget.
from matplotlib.backends.backend_qt5agg \
 import FigureCanvasQTAgg as FigureCanvas   # is a pure Qt Widget object


class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class MplWidget(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.canvas = MplCanvas()
        self.vbl = QtWidgets.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
