import sys
from PyQt6 import QtWidgets, uic
  
app = QtWidgets.QApplication(sys.argv)

window = uic.loadUi("Start.ui")
window.show()
app.exec()