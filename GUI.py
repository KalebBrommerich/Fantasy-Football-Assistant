#Using Python 3.12.2 64-bit
#Found a decent web framework called Flask  pip install Flask
#https://flask.palletsprojects.com/en/3.0.x/quickstart/
#Built in Python GUI seems kinda bad according to internet
#but thats too complex for now
#pip install pyqt6
#https://doc.qt.io/qtforpython-6/index.html

import Webscraper as ws
from PySide6 import QtCore, QtWidgets, QtGui
import sys
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.scrape)


    @QtCore.Slot()
    def magic(self):
        self.text.setText("Test")

    def scrape(self):
        ws.Webscraper("https://www.pro-football-reference.com/years/2023/passing.htm","passing").scrape_table()

    def update_text(self):
        self.text.setText("Test")
    


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.showMaximized()
    widget.show()

    sys.exit(app.exec())