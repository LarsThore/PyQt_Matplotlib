#! encoding:utf8 #

import numpy as np

from PyQt5 import QtGui
from PyQt5 import QtWidgets

# Matplolib figure object
from matplotlib.figure import Figure

# import the Qt5Agg FigureCanvas object, that binds Figure to Qt5Agg
# backend. It also inherits from QWidget.
from matplotlib.backends.backend_qt5agg \
 import FigureCanvasQTAgg as FigureCanvas   # is a pure Qt Widget object

import psutil as p

# total number of iterations
maxiters = 30

class CPUMonitor(FigureCanvas):
    ''' Matplotlib Figure widget to display CPU utilization.'''
    def __init__(self):
        # save the current CPU info (used by updating algorithm)
        self.before = self.prepare_cpu_usage()

        # first image setup
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        # initialization of the canvas
        FigureCanvas.__init__(self, self.fig)

        # set specific limits for the x- and y-axes
        self.ax.set_xlim(0, 30)
        self.ax.set_ylim(0, 100)

        # disable figure-wide autoscale
        self.ax.set_autoscale_on(False)

        # generate first empty plots
        self.user = []
        self.nice = []
        self.sys = []
        self.idle = []

        # draw placeholder lines for the four data sets
        self.l_user, = self.ax.plot([], self.user, label = 'User %')
        self.l_nice, = self.ax.plot([], self.nice, label = 'Nice %')
        self.l_sys, = self.ax.plot([], self.sys, label = 'Sys %')
        self.l_idle, = self.ax.plot([], self.idle, label = 'Idle %')

        # add legend to plot
        self.ax.legend()

        # force redraw of the figure
        self.fig.canvas.draw()

        # initialize the iteration counter
        self.cnt = 0

        # call the update method (to speed up visualization)
        self.timerEvent(None)

        # start timer, trigger event every 1000 milliseconds (= 1 sec)
        self.timer = self.startTimer(1000)

    def prepare_cpu_usage(self):
        '''helper function to return CPU usage info'''

        # get the CPU times using psutil module
        t = cpu_times()

        # return only the values we are interested in
        if hasattr(t, 'nice'):
            return [t.user, t.nice, t.system, t.idle]
        else:
            # special case for Windows, without 'nice' value
            return [t.user, 0, t.system, t.idle]


    def get_cpu_usage(self):
        '''compute CPU usage comparing previous and current measurements'''

        # take the current CPU usage information
        now = self.prepare_cpu_usage()

        # compute dleta between current and previous measurements
        delta = [now[i]-self.before[i] for i in range(len(now))]

        # compute the total (needed for percentage calculation)
        total = sum(delta)

        # save the current measurement to before object
        self.before = now

        # retrun the percentage of CPU usage for our four categories
        return [(100.0*dt)/total for dt in delta]

    def timerEvent(self, evt):
        '''Custom timerEvent code, called at timer event receive'''

        # get the CPU percentage usage
        result = self.get_cpu_usage()

        # append new data to the datasets
        self.user.append(result[0])
        self.nice.append(result[1])
        self.sys.append(result[2])
        self.idle.append(result[3])

        # replot the lines with updated information
        self.l_user.set_data(range(len(self.user)), self.user)
        self.l_nice.set_data(range(len(self.nice)), self.nice)
        self.l_sys.set_data(range(len(self.sys)), self.sys)
        self.l_idle.set_data(range(len(self.idle)), self.idle)

        # force a redraw of the Figure
        self.fig.canvas.draw()

        # if we have done all the iterations
        if self.cnt == maxiters:
            # stop the timer
            self.killTimer(self.timer)
        else:
            # else, we increment the counter
            self.cnt += 1


# Create the GUI application
app = QtWidgets.QApplication(sys.argv)
''' Note: Every PyQt application must create one and only one QApplication
instance, no matter how many windows compose the application.
Since QApplication handles the entire initialization phase it must be created
before any other objects related to the UI are created.'''

# Create the Matplotlib widget
widget = CPUMonitor()

widget.setWindowTitle("30 Seconds of CPU Usage Updated in Realtime")

# show the widget
widget.show()

# start with main Qt main loop execution, exiting from this script with the
# same return code of Qt application
sys.exit(qApp.exec_())
