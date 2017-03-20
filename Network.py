#! -*- coding: utf-8 -*- #

from PyQt5.QtCore import Qt, QRectF, QEvent
from PyQt5.QtGui import QColor, QPen, QBrush, QImage, QPainter
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QLabel
from PyQt5.uic import loadUi

from types import MethodType
import sys
import numpy as np

app = QApplication(sys.argv)
__appname__ = "Red Network"

##################### importing the file made qt designer #####################
w = loadUi("Network_Gui.ui")

#################### image for saving the picture of circles ##################
img = QImage(w.widget.width(), w.widget.height(), QImage.Format_RGB32)
img.fill(Qt.white)              # image appears white in the beginning (not black)

################################ set imgpainter ##################################
node_painter = QPainter()         # painter for painting nodes
imgpainter = QPainter()            # painter for drawing image

################################## set pen ####################################
line_drawer = QPen()            # pen for drawing edges
line_drawer.setWidth(4)

############################ set switch and lists #############################
switch = 0      # switch at 0 for first node, at 1 for second node
edge_counter = 0

total_edge_length = 0

start_point_list = [0]
end_point_list = [0]
coordinate_set = set()

midpoints = []
edges = []

############################### help functions ################################

def export_nodes():
    """
    Uses the global list 'midpoints' to export the data points of the nodes,
    so that they can be saved as a .txt file.
    """
    fileObj = QFileDialog.getSaveFileName(w)

    print (fileObj)
    print (type(fileObj))

    header = "Node positions \n \nx-coordinates \ty-coordinates \n"
    content = ""

    for point in midpoints:
        content += str(point.x()) + "\t" + str(point.y()) + "\n"

    fileName = fileObj[0]

    with open(fileName, "w") as file:
        file.write(header + content)

def export_edges():
    """
    Uses the global list 'edges' to export the data points of the edges,
    so that they can be saved as a .txt file.
    """
    fileObj = QFileDialog.getSaveFileName(w)

    header = "Edge positions \n \nStart Point (x, y) \tEnd Point (x, y)\n \n"
    content = ""

    for tupel in edges:
        counter = 0
        for edge in tupel:
            if counter % 2 == 0:
                content += str(edge.x()) + "\t" + str(edge.y()) + "\t"
            else:
                content += str(edge.x()) + "\t" + str(edge.y()) + "\n"
            counter += 1

    fileName = fileObj[0]

    with open(fileName, "w") as file:
        file.write(header + content)

def draw_circles(x, y):
    """
    Takes the x and y data of the event (mouse click) and draws a circle with
    the QPainter 'imgpainter' around that point with the radius (r) 10.
    """
    print ( tuple((x, y)) ),

    r = 10
    node_painter.begin(img)          # use first imgpainter to draw on image
    node_painter.setBrush(Qt.red)
    node_painter.drawEllipse(x-r, y-r, 2*r, 2*r)    # draw circle (circles are represented as an ellipse)
    node_painter.end()

def fill_coordinate_set(x, y):
    """
    Takes the x and y data of the event (mouse click) and fills the set
    'coordinate_set' with all the data points that surround this midpoint
    """
    for x_distance in range(-10, 11):            # set that will contain all pixels inside the circle
        for y_distance in range(-10, 11):        # (or still inside a square around the circle center)
            coordinate_set.add(tuple((x + x_distance, y + y_distance)))

def find_closest_midpoint(event):
    """
    Takes the event (mouse click) and puts the start or end point of an edge
    directly onto the corresponding midpoint of a node. So all the edges start
    and end exactly in the middle of each node.
    """
    diff_list = []

    for position in midpoints:
        diff0 = abs(position.x() - event.pos().x())
        diff1 = abs(position.y() - event.pos().y())
        diff_list.append(np.sqrt(diff0**2 + diff1**2))

    diff_array = np.array(diff_list)
    i = np.argmin(diff_array)

    return  midpoints[i]

def save_starting_point(event):
    '''
    saves the starting point of the line after a click on the widget
    '''

    start_point = find_closest_midpoint(event)
    print ("start")
    start_point_list[0] = start_point

def calculate_edge_length(end_point_list):
    """
    Takes the current end point - which is saved as only member in the list
    'end_point_list' - and the start point as the only member of the global
    list 'start_point_list' and calculates the corresponding distance after
    Pythagoras.
    The distances are accumulated in the variable 'total_edge_length'.
    """
    global total_edge_length

    start = start_point_list[0]
    end = end_point_list[0]

    x_diff = abs(start.x() - end.x())
    y_diff = abs(start.y() - end.y())

    distance = np.sqrt(x_diff**2 + y_diff**2)
    total_edge_length += distance

def draw_line(event):
    '''
    uses the starting point and the second point - which is indicated by
    another click - to draw a line between those points
    '''

    end_point = find_closest_midpoint(event)
    print ("end")
    if end_point == start_point_list[0]:
        raise ValueError("Start point and end point are equal.")
    end_point_list[0] = end_point

    edges.append( tuple((start_point_list[0], end_point_list[0])) )

    # start_point_list[0] = end_point

    node_painter.begin(img)          # use node_painter to draw on image
    node_painter.setPen(line_drawer)
    node_painter.drawLine(start_point_list[0], end_point)    # draw line from first circle to second circle
    node_painter.end()

    calculate_edge_length(end_point_list)

############################### main function #################################

def drawing(self, event):
    print (event.type())
    global switch, edge_counter

    print (event.type() == QEvent.MouseButtonPress and
            tuple((event.pos().x(), event.pos().y())) not in coordinate_set)

    # True if mouse click happens with cursor on free surface
    if (event.type() == QEvent.MouseButtonPress and
        tuple((event.pos().x(), event.pos().y())) not in coordinate_set):

        try:
            print (w.comboBox.currentIndex())
            if w.comboBox.currentIndex() == 0 or w.comboBox.currentIndex() == 1:
                midpoints.append(event.pos())
                circle_center = event.pos()
                x = circle_center.x()
                y = circle_center.y()

                draw_circles(x, y)
                fill_coordinate_set(x, y)       # set value to dictionary key 'circle center'
                self.update()                   # requests a paint event

                w.node_label.setText("Nodes:\n" + str(len(midpoints)))
            else:
                raise Exception
        except Exception:
            print ("Edge mode - not possible to draw nodes in this mode")

    # True if mouse click happens with cursor on a node (and switch == 0)
    elif (event.type() == QEvent.MouseButtonPress and switch == 0 and
            tuple((event.pos().x(), event.pos().y())) in coordinate_set):

        try:
            if w.comboBox.currentIndex() == 0 or w.comboBox.currentIndex() == 2:
                save_starting_point(event)
                switch = 1
                print ("switch: ", switch)
            else:
                raise Exception
        except Exception:
            print ("Node mode - not possible to draw edges in this mode")

    # True if mouse click happens with cursor on a node (and switch == 1)
    elif (event.type() == QEvent.MouseButtonPress and switch == 1 and
            tuple((event.pos().x(), event.pos().y())) in coordinate_set):

        try:
            draw_line(event)
            self.update()                           # requests a paint event
            switch = 0
            print ("switch: ", switch)

            edge_counter += 1
            w.edge_label.setText("Edges:\n" + str(edge_counter))
            w.total_length_label.setText("Total edge length:\n" + str(int(total_edge_length)))

        except ValueError:
            pass

    # True if 'self.update()' is called
    elif event.type() == QEvent.Paint:          # (you're only allowed to draw here (in a paint event) ?)
        imgpainter.begin(self)                  # use imgpainter to draw image on widget
        imgpainter.drawImage(0, 0, img)
        imgpainter.end()

    return True                                 # return 'True' so that the event handler
                                                # knows that the event is completed


def erase():
    '''
    Deletes all Nodes and Edges and resets all lists and counters to the default
    values.
    '''

    global switch, edge_counter, total_edge_length, start_point_list
    global end_point_list, coordinate_set, midpoints, edges

    switch = 0
    edge_counter = 0
    total_edge_length = 0
    start_point_list = [0]
    end_point_list = [0]
    coordinate_set = set()
    midpoints = []
    edges = []

    img.fill(Qt.white)
    w.widget.update()
    w.node_label.setText("Nodes:\n" + str(len(midpoints)))
    w.edge_label.setText("Edges:\n" + str(len(edges)))
    w.total_length_label.setText("Total edge length:\n" + str(total_edge_length))


if __name__ == '__main__':
    w.widget.event = MethodType(drawing, w.widget)  # ersetzt die Funktion, die die Ereignisse behandelt

    w.eraseButton.clicked.connect(erase)
    w.Export_Nodes.clicked.connect(export_nodes)
    w.Export_Edges.clicked.connect(export_edges)

    # w.comboBox.currentIndexChanged.connect(w.update())

    w.show()
    sys.exit(app.exec_())
