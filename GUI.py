#Using Python 3.12.2 64-bit
#Found a decent web framework called Flask  pip install Flask
#https://flask.palletsprojects.com/en/3.0.x/quickstart/
#but thats too complex for now
#pip install pyside6
#https://doc.qt.io/qtforpython-6/index.html

import Webscraper as ws
import WebscraperExperts as wse
from PySide6 import QtCore, QtWidgets, QtGui
import sys, time, asyncio, csv, threading, time, os

class MyWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fantasy Football Assistant")
        self.ScrapeBtn = QtWidgets.QPushButton("Scrape tables")
        self.ClearCacheBtn = QtWidgets.QPushButton("Clear cache")
        self.LoadArchivedDataBtn = QtWidgets.QPushButton("Load Archived Data")
        self.GenRankingsBtn = QtWidgets.QPushButton("Generate rankings")
        self.ViewRankingsBtn = QtWidgets.QPushButton("Compare players") 
        self.EnterModifiersBtn = QtWidgets.QPushButton("Enter modifiers") 
        self.TableTitle = QtWidgets.QLabel("Predictions for next year")
        
        self.layout = QtWidgets.QVBoxLayout(self)

        tables = QtWidgets.QHBoxLayout()
        self.table = QtWidgets.QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.showGrid
        #init, just having it read a file for now
        self.loadTable(self.table,".\\welcome.csv" )

        tables = QtWidgets.QHBoxLayout()
        self.table2 = QtWidgets.QTableWidget()
        self.table2.setAlternatingRowColors(True)
        self.table2.showGrid

        
        #init, just having it read a file for now
        self.loadTable(self.table2,".\\ranking-table.csv" )
        self.table2.setColumnWidth(1,150)
        tables.addWidget(self.table)
        tables.addWidget(self.table2)


        self.layout.addWidget(self.TableTitle,alignment=QtCore.Qt.AlignCenter)
        self.layout.addLayout(tables)

        home = QtWidgets.QHBoxLayout()
        home.addWidget(self.ScrapeBtn, alignment=QtCore.Qt.AlignBottom) 
        home.addWidget(self.ClearCacheBtn, alignment=QtCore.Qt.AlignBottom)     
        home.addWidget(self.GenRankingsBtn, alignment=QtCore.Qt.AlignBottom) 
        home.addWidget(self.EnterModifiersBtn, alignment=QtCore.Qt.AlignBottom)
        home.addWidget(self.LoadArchivedDataBtn, alignment=QtCore.Qt.AlignBottom)

        self.layout.addLayout(home)
        
        self.ScrapeBtn.clicked.connect(self.scrape)
        self.EnterModifiersBtn.clicked.connect(self.modPopup)
        self.LoadArchivedDataBtn.clicked.connect(self.arcPopup)

    @QtCore.Slot()

    def scrape(self):
        #scrape all the tables
        for year in range(2023,2024 ):
            t1 = threading.Thread(target=ws.Webscraper("https://www.pro-football-reference.com/years/"+str(year)+"/passing.htm","passing")
                              .scrape_table_to_csv,args=("https://www.pro-football-reference.com/years/"+str(year)+"/passing.htm",str(year)+"\\passing.csv"),name="t1")
            t2 = threading.Thread(target=ws.Webscraper("https://www.pro-football-reference.com/years/"+str(year)+"/rushing.htm","rushing")
                              .scrape_table_to_csv,args=("https://www.pro-football-reference.com/years/"+str(year)+"/rushing.htm",str(year)+"\\rushing.csv"), name="t2")
            t3 = threading.Thread(target=ws.Webscraper("https://www.pro-football-reference.com/years/"+str(year)+"/receiving.htm", "receiving")
                              .scrape_table_to_csv,args=("https://www.pro-football-reference.com/years/"+str(year)+"/receiving.htm", str(year)+"\\receiving.csv"), name="t3")
            t4 = threading.Thread(target=ws.Webscraper("https://www.pro-football-reference.com/years/"+str(year)+"/scrimmage.htm","receiving_and_rushing")
                              .scrape_table_to_csv,args=("https://www.pro-football-reference.com/years/"+str(year)+"/scrimmage.htm",str(year)+"\\receiving_and_rushing.csv"),name="t4")
        
            t1.start()
            print("started 1",year)
            t2.start()
            print("started 2",year)
            t3.start()
            print("started 3",year)
            t4.start()
            print("started 4",year)

            print("started experts")
            wse.WebscraperExperts("https://www.fantasypros.com/nfl/fantasy-football-rankings.php","ranking-table").scrape_table_to_csv("ranking-table","ranking-table.csv")
            print("finished experts")
            
            t1.join()
            print("Joined 1",year)
            t2.join()
            print("Joined 2",year)
            t3.join()
            print("Joined 3",year)
            t4.join()
            print("Joined 4",year)   



    def clearCache(self):
        time.sleep(1)
    def genRankings(self):
        time.sleep(1)

    def modPopup(self):
        dlg = ModifiersPopup()
        dlg.exec()
    def arcPopup(self):
        print(self.TableTitle.text())
        dlg = ArchivedDataPopup(True if self.TableTitle.text() == "Predictions for next year" else False)
        dlg.exec()
        if(dlg.year != ""):
            if(dlg.usePred.isChecked()):
               #load predictions result
               self.TableTitle.setText("Predictions for next year")
            else:
                #load archived data that was selected
                self.loadTable(self.table,os.curdir+"\\TrainingData"+"\\"+dlg.year+"\\"+dlg.dataset+".csv")
                self.TableTitle.setText(dlg.year+ " " + dlg.dataset)


            

    def loadTable(self, table, file):
        with open(file ,encoding="utf-8") as csvFile:
            csvReader = csv.reader(csvFile)
            data =  list(csvReader)

            rowData = list(data)
            table.setRowCount(len(data))
            table.setColumnCount(len(rowData[0]))
            offset = 0
            for rowIdx, rowData in enumerate(data):
                if(rowData[0]=="Rk" and rowIdx !=0):
                    offset+=1
                    continue
                #nested loop
                for colIdx, colData in enumerate(rowData):
                    table.setItem(rowIdx-offset,colIdx,QtWidgets.QTableWidgetItem(colData))
            table.resizeColumnsToContents()        
class ArchivedDataPopup(QtWidgets.QDialog):

    def __init__(self,UsePred):
        super().__init__()
        print(UsePred)
        self.year = ""
        self.dataset =""
        QBtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Select year and data you want to view")
        
        self.enter1 =  QtWidgets.QHBoxLayout()
        self.txt1 = QtWidgets.QLabel("Year: ")
        self.in1 = QtWidgets.QComboBox()
        self.in1.addItems( os.listdir(os.curdir+"\\TrainingData"))
        self.enter1.addWidget(self.txt1)
        self.enter1.addWidget(self.in1)

        self.enter2 =  QtWidgets.QHBoxLayout()
        self.txt2 = QtWidgets.QLabel("Data set: ")
        self.in2 = QtWidgets.QComboBox()
        self.in2.addItems(["passing","reveiving","rushing"])
        self.enter2.addWidget(self.txt2)
        self.enter2.addWidget(self.in2)

        self.usePred = QtWidgets.QRadioButton("Display predictions for next year", self)
        self.useArchived = QtWidgets.QRadioButton("Display archived data", self)
        if(UsePred):
            self.usePred.setChecked(True)
        else:
            self.useArchived.setChecked(True)

        self.layout.addWidget(message)
        self.layout.addLayout(self.enter1)
        self.layout.addLayout(self.enter2)
        self.layout.addWidget(self.usePred,alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.useArchived,alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.buttonBox,alignment=QtCore.Qt.AlignCenter)
        
        self.setLayout(self.layout)
    def accept(self):
        print("Accept")
        self.year = self.in1.currentText()
        self.dataset = self.in2.currentText()
        print(self.year,self.dataset)
        self.close()


#inheritance
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


        #https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QLineEdit.html#PySide6.QtWidgets.PySide6.QtWidgets.QLineEdit.inputMask
        self.enter1 =  QtWidgets.QHBoxLayout()
        txt1 = QtWidgets.QLabel("Something: ")
        in1 = QtWidgets.QLineEdit()
        in1.setInputMask("00")
        self.enter1.addWidget(txt1)
        self.enter1.addWidget(in1)

        self.enter2 =  QtWidgets.QHBoxLayout()
        txt2 = QtWidgets.QLabel("Something: ")
        in2 = QtWidgets.QLineEdit()
        in2.setInputMask("00")
        self.enter2.addWidget(txt2)
        self.enter2.addWidget(in2)

        self.enter3 =  QtWidgets.QHBoxLayout()
        txt3 = QtWidgets.QLabel("Something: ")
        in3 = QtWidgets.QLineEdit()
        in3.setInputMask("00")
        self.enter3.addWidget(txt3)
        self.enter3.addWidget(in3)

        self.enter4 =  QtWidgets.QHBoxLayout()
        txt4 = QtWidgets.QLabel("Something: ")
        in4 = QtWidgets.QLineEdit()
        in4.setInputMask("00")
        self.enter4.addWidget(txt4)
        self.enter4.addWidget(in4)


        self.layout.addWidget(message)
        self.layout.addLayout(self.enter1)
        self.layout.addLayout(self.enter2)
        self.layout.addLayout(self.enter3)
        self.layout.addLayout(self.enter4)
        self.layout.addWidget(self.buttonBox,alignment=QtCore.Qt.AlignCenter)
        self.setLayout(self.layout)

    def accept(self):
        print("accept")
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.setMinimumSize(800,600)
    widget.showMaximized()
    
    sys.exit(app.exec())