#! encoding:utf8 #

import sys
import numpy as np

from PyQt5 import QtGui
from PyQt5 import QtWidgets

# Matplolib figure object
from matplotlib.figure import Figure

# import the Qt5Agg FigureCanvas object, that binds Figure to Qt5Agg
# backend. It also inherits from QWidget.
from matplotlib.backends.backend_qt5agg \
 import FigureCanvasQTAgg as FigureCanvas   # is a pure Qt Widget object

class Qt5MplCanvas(FigureCanvas):
    ''' Class to represent the FigureCanvas widget.'''
    def __init__(self):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        self.x = np.arange(0.0, 3.0, 0.01)
        self.y = np.cos(2*np.pi*self.x)
        self.axes.plot(self.x, self.y)

        # take the matplotlib figure object and render it in a Qt widget
        FigureCanvas.__init__(self, self.fig)


# Create the GUI application
qApp = QtWidgets.QApplication(sys.argv)
''' Note: Every PyQt application must create one and only one QApplication
instance, no matter how many windows compose the application.
Since QApplication handles the entire initialization phase it must be created
before any other objects related to the UI are created.'''

# Create the Matplotlib widget
mpl = Qt5MplCanvas()

# show the widget
mpl.show()

# start with main Qt main loop execution, exiting from this script with the
# same return code of Qt application
sys.exit(qApp.exec_())
