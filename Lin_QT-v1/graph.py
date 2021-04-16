import sys
import time

from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader

import numpy as np

from matplotlib.backends.qt_compat import QtCore, QtWidgets

if QtCore.qVersion() >= "5.":
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure
import PySide2.Q

#继承于mainwindow 类，只偶此类才有tool bar
class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = QUiLoader().load('u3.ui')
        self.ui.pushButton.clicked.connect(self.testpopwindow)
        #生成一个widget，放在mainwindow 中间
        self._main = QtWidgets.QWidget()

        self.setCentralWidget(self._main)

        #继承自父类，_main，即删除_main layout也会删除
        #下面两幅画都是在layout下
        layout = QtWidgets.QVBoxLayout(self._main)

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(static_canvas)
        self.addToolBar(NavigationToolbar(static_canvas, self))

        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(dynamic_canvas)
        self.addToolBar(QtCore.Qt.BottomToolBarArea,
                        NavigationToolbar(dynamic_canvas, self))

        self._static_ax = static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self._static_ax.plot(t, np.tan(t), ".")

        self._dynamic_ax = dynamic_canvas.figure.subplots()
        t = np.linspace(0, 10, 101)
        # Set up a Line2D.
        self._line, = self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self._timer = dynamic_canvas.new_timer(50)
        self._timer.add_callback(self._update_canvas)
        self._timer.start()

    def  testpopwindow(self):
        self.show()

    def _update_canvas(self):
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._line.set_data(t, np.sin(t + time.time()))
        self._line.figure.canvas.draw()


if __name__ == "__main__":
    # Check whether there is already a running QApplication (e.g., if running
    # from an IDE).
    qapp = QApplication.instance()
    if not qapp:
        qapp = QApplication(sys.argv)

    app = ApplicationWindow()
    app.ui.show()
    app.activateWindow()
    app.raise_()
    qapp.exec_()