import sys
from PyQt5 import QtWidgets, uic
  
app = QtWidgets.QApplication(sys.argv)

window = uic.loadUi("Sources.ui")
window.show()
app.exec()