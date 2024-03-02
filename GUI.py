#Using Python 3.12.2 64-bit
#Found a decent web framework called Flask  pip install Flask
#https://flask.palletsprojects.com/en/3.0.x/quickstart/
#Built in Python GUI seems kinda bad according to internet
#but thats too complex for now
#pip install pyqt6
#https://doc.qt.io/qtforpython-6/index.html

import Webscraper as ws
from PySide6 import QtCore, QtWidgets, QtGui
import sys, time, asyncio, csv

class MyWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fantasy Football Assistant")
        self.ScrapeBtn = QtWidgets.QPushButton("Scrape tables")
        self.ClearCacheBtn = QtWidgets.QPushButton("Clear cache")
        self.GenRankingsBtn = QtWidgets.QPushButton("Generate rankings")
        center = QtWidgets.QWidget()
        
        self.table = QtWidgets.QTableWidget()
        
        self.table.setAlternatingRowColors(True)
        self.table.showGrid
        #init, just having it read a file for now
        self.loadTable(self.table,"C:\\Users\\ei5252ec\\git\\Fantasy-Football-Assistant\\passing.csv" )
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.table)

        temp = QtWidgets.QHBoxLayout()
        temp.addWidget(self.ScrapeBtn, alignment=QtCore.Qt.AlignBottom) 
        temp.addWidget(self.ClearCacheBtn, alignment=QtCore.Qt.AlignBottom)     
        temp.addWidget(self.GenRankingsBtn, alignment=QtCore.Qt.AlignBottom) 
        self.layout.addLayout(temp)

        self.ScrapeBtn.clicked.connect(self.scrape)



    @QtCore.Slot()


    def scrape(self):
        #scrape all the tables
        self.ScrapeBtn.setText("Aadas")
        self.ScrapeBtn.addAction
        self.text.setText("ASDasda")
        #ws.Webscraper("https://www.pro-football-reference.com/years/2023/passing.htm","passing").scrape_table()
        time.sleep(1)
        self.ScrapeBtn.setText("Scrape tables")
    def clearCache(self):
        time.sleep(1)
    def genRankings(self):
        time.sleep(1)
    #maybe move this method into a different file?
    def loadTable(self, table, file):
        with open(file ,encoding="utf-8") as csvFile:
            csvReader = csv.reader(csvFile)
            data =  list(csvReader)

            self.table.setRowCount(len(data))
            self.table.setColumnCount(len(data))
            for rowIdx, rowData in enumerate(data):
                for colIdx, colData in enumerate(rowData):
                    self.table.setItem(rowIdx,colIdx,QtWidgets.QTableWidgetItem(colData))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.showMaximized()
    widget.show()

    sys.exit(app.exec())