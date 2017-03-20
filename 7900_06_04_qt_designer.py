#! encoding:utf8 #

import numpy as np

import sys

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from qtdesigner import Ui_MplMainWindow

class DesignerMainWindow(QtWidgets.QMainWindow, Ui_MplMainWindow):
    def __init__(self, parent = None):
        super(DesignerMainWindow, self).__init__(parent)
        self.setupUi(self)

        # QtCore.QObject.connect(self.mplpushButton, QtCore.SIGNAL("clicked()"), self.update_graph)
        # QtCore.QObject.connect(self.mplactionOpen, QtCore.SIGNAL('triggered()'), self.select_file)
        # QtCore.QObject.connect(self.mplactionQuit, QtCore.SIGNAL('triggered()'), QtGui.qApp,
        #     QtCore.SLOT("quit()"))

        self.mplpushButton.clicked.connect(self.update_graph)
        self.mplactionOpen.triggered.connect(self.select_file)
        # self.mplactionQuit.triggered.connect(QtGui.qApp.quit())


    def select_file(self):
        file_open = QtWidgets.QFileDialog.getOpenFileName()
        file = file_open[0]

        if file:
            self.mpllineEdit.setText(file)

    def parse_file(self, filename):
        letters = {}

        for i in range(97, 122 + 1):
            letters[chr(i)] = 0

        with open(filename) as f:
            for line in f:
                for char in line:
                    # counts only letters
                    if ord(char.lower()) in range(97, 122 + 1):
                        letters[char.lower()] += 1

        k = sorted(letters.keys())
        v = [letters[ki] for ki in k]
        return k, v

    def update_graph(self):
        l, v= self.parse_file(self.mpllineEdit.text())

        self.mpl.canvas.ax.clear()
        self.mpl.canvas.ax.bar(np.arange(len(l)) - 0.25, v, width = 0.5)
        self.mpl.canvas.ax.set_xticks(range(len(l)))
        self.mpl.canvas.ax.set_xticklabels(l)
        self.mpl.canvas.ax.get_yaxis().grid(True)
        self.mpl.canvas.draw()


app = QtWidgets.QApplication(sys.argv)
dmw = DesignerMainWindow()
dmw.show()
sys.exit(app.exec_())














#
