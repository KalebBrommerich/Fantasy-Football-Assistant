#Using Python 3.12.2 64-bit
#Found a decent web framework called Flask  pip install Flask
#https://flask.palletsprojects.com/en/3.0.x/quickstart/
#Built in Python GUI seems kinda bad according to internet
#but thats too complex for now
#pip install pyside6
#https://doc.qt.io/qtforpython-6/index.html

import Webscraper as ws
from PySide6 import QtCore, QtWidgets, QtGui
import sys, time, asyncio, csv, threading

class MyWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fantasy Football Assistant")
        self.ScrapeBtn = QtWidgets.QPushButton("Scrape tables")
        self.ClearCacheBtn = QtWidgets.QPushButton("Clear cache")
        self.GenRankingsBtn = QtWidgets.QPushButton("Generate rankings")
        self.ViewRankingsBtn = QtWidgets.QPushButton("Compare players") 
        self.EnterModifiersBtn = QtWidgets.QPushButton("Enter modifiers") 
        
        self.table = QtWidgets.QTableWidget()
        
        self.table.setAlternatingRowColors(True)
        self.table.showGrid
        #init, just having it read a file for now
        self.loadTable(self.table,".\\passing.csv" )
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.table)

        home = QtWidgets.QHBoxLayout()
        home.addWidget(self.ScrapeBtn, alignment=QtCore.Qt.AlignBottom) 
        home.addWidget(self.ClearCacheBtn, alignment=QtCore.Qt.AlignBottom)     
        home.addWidget(self.GenRankingsBtn, alignment=QtCore.Qt.AlignBottom) 
        home.addWidget(self.EnterModifiersBtn, alignment=QtCore.Qt.AlignBottom)
        self.layout.addLayout(home)
        
        self.ScrapeBtn.clicked.connect(self.scrape)
        self.EnterModifiersBtn.clicked.connect(self.modPopup)




    @QtCore.Slot()

    def scrape(self):
        #scrape all the tables
        self.ScrapeBtn.setText("Aadas")
        t1 = threading.Thread(target=ws.Webscraper("https://www.pro-football-reference.com/years/2023/passing.htm","passing")
                              .scrape_table_to_csv,args=("https://www.pro-football-reference.com/years/2023/passing.htm","passing.csv"),name="t1")
        t2 = threading.Thread(target=ws.Webscraper("https://www.pro-football-reference.com/years/2023/rushing.htm","rushing")
                              .scrape_table_to_csv,args=("https://www.pro-football-reference.com/years/2023/rushing.htm", "rushing.csv"), name="t2")
        t3 = threading.Thread(target=ws.Webscraper("https://www.pro-football-reference.com/years/2023/receiving.htm", "receiving")
                              .scrape_table_to_csv,args=("https://www.pro-football-reference.com/years/2023/receiving.htm", "receiving.csv"), name="t3")
        t4 = threading.Thread(target=ws.Webscraper("https://www.pro-football-reference.com/years/2023/scrimmage.htm","receiving_and_rushing")
                              .scrape_table_to_csv,args=("https://www.pro-football-reference.com/years/2023/scrimmage.htm","receiving_and_rushing.csv"),name="t4")
        
        t1.start()
        print("started 1")
        t2.start()
        print("started 2")
        t3.start()
        print("started 3")
        t4.start()
        print("started 4")

        t1.join()
        print("Joined 1")
        t2.join()
        print("Joined 2")
        t3.join()
        print("Joined 3")
        t4.join()
        print("Joined 4")

    def clearCache(self):
        time.sleep(1)
    def genRankings(self):
        time.sleep(1)
    #maybe move this method into a different file?
        
    def modPopup(self):
        dlg = ModifiersPopup()
        dlg.exec()

    def loadTable(self, table, file):
        with open(file ,encoding="utf-8") as csvFile:
            csvReader = csv.reader(csvFile)
            data =  list(csvReader)

            self.table.setRowCount(len(data))
            self.table.setColumnCount(len(data))
            for rowIdx, rowData in enumerate(data):
                for colIdx, colData in enumerate(rowData):
                    self.table.setItem(rowIdx,colIdx,QtWidgets.QTableWidgetItem(colData))

class ModifiersPopup(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Point Modifiers")

        QBtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Enter the point modifiers for your league:")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox,alignment=QtCore.Qt.AlignCenter)
        self.setLayout(self.layout)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.setMinimumSize(800,600)
    widget.showMaximized()
    

    sys.exit(app.exec())