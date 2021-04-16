import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader

class mywindows:
    def __init__(self):
        #GUI 动态载入
        self.ui = QUiLoader().load('u3.ui')
        self.ui1 = QUiLoader().load('u4.ui')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = mywindows()
    demo.ui.show()
    demo.ui1.show()
    sys.exit(app.exec_())