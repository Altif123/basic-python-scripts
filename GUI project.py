from PyQt5 import QtCore, uic, QtWidgets

import sys

UIClass, QtBaseClass = uic.loadUiType("gui.ui")

class MyApp(UIClass, QtBaseClass):
    def __init__(self):
        UIClass.__init__(self)
        QtBaseClass.__init__(self)
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())