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
        self.RushingReceivingTD = 0
        self.RushingReceivingYD = 0
        self.PassingTD = 0
        self.PPR = 0
        self.Interceptions = 0
        self.PassingYd = 0
        self.setWindowTitle("Fantasy Football Assistant")

        #buttons for doing operations with the data
        self.ScrapeBtn = QtWidgets.QPushButton("Scrape tables")
        self.ClearCacheBtn = QtWidgets.QPushButton("Clear cache")
        self.LoadArchivedDataBtn = QtWidgets.QPushButton("Load Archived Data")
        self.GenRankingsBtn = QtWidgets.QPushButton("Generate rankings")

        #table titles
        self.EnterModifiersBtn = QtWidgets.QPushButton("Enter modifiers") 
        self.TableTitleLeft = QtWidgets.QLabel("Predictions for next year")
        self.TableTitleRight = QtWidgets.QLabel("Expert consensus")
        
        self.layout = QtWidgets.QVBoxLayout(self)

        #tables layout
        tables = QtWidgets.QHBoxLayout()

        #init right table
        self.table = QtWidgets.QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.showGrid
        self.loadTable(self.table,".\\welcome.csv" )

        #init experts table
        self.table2 = QtWidgets.QTableWidget()
        self.table2.setAlternatingRowColors(True)
        self.table2.showGrid()
        self.loadTable(self.table2,".\\ranking-table.csv" )
        self.table2.setColumnWidth(1,150)

        #add tables to table layout
        tables.addWidget(self.table)
        tables.addWidget(self.table2)
        
        #create table titles
        header = QtWidgets.QHBoxLayout()
        header.addWidget(self.TableTitleLeft,alignment=QtCore.Qt.AlignCenter)
        header.addWidget(self.TableTitleRight,alignment=QtCore.Qt.AlignCenter)

        #create for each operation
        home = QtWidgets.QHBoxLayout()
        home.addWidget(self.ScrapeBtn, alignment=QtCore.Qt.AlignBottom) 
        home.addWidget(self.ClearCacheBtn, alignment=QtCore.Qt.AlignBottom)     
        home.addWidget(self.GenRankingsBtn, alignment=QtCore.Qt.AlignBottom) 
        home.addWidget(self.EnterModifiersBtn, alignment=QtCore.Qt.AlignBottom)
        home.addWidget(self.LoadArchivedDataBtn, alignment=QtCore.Qt.AlignBottom)

        #add everything to the GUI
        self.layout.addLayout(header)
        self.layout.addLayout(tables)
        self.layout.addLayout(home)
        
        #make buttons execute methods when clicked
        self.ScrapeBtn.clicked.connect(self.scrape)
        self.EnterModifiersBtn.clicked.connect(self.modPopup)
        self.LoadArchivedDataBtn.clicked.connect(self.arcPopup)
        self.readScoringConfig()

    @QtCore.Slot()

    def scrape(self):
        #scrape all the tables
        #the range can be changed and works for (most) years, tried back to 2003
        for year in range(2023,2024 ):
            #create and execute threads for each stat table
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

            #get expert data after all other threads start
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

    #Popup for entering scoring settings
    def modPopup(self):
        self.readScoringConfig()
        #pass params to pre-set data fields
        dlg = ModifiersPopup(self.RushingReceivingTD,self.RushingReceivingYD,self.PassingTD, self.PPR,self.Interceptions,self.PassingYd)
        dlg.exec()
        #if accepted, re-write file with new settings, else continue
        if(dlg.accepted):
            self.writeScoringConfig(dlg.in1.text(),dlg.in2.text(),dlg.in3.text(),dlg.in4.text(),dlg.in5.text(),dlg.in6.text())

    def arcPopup(self):
        #inline check to see what is currently being displayed to preselect radio button
        dlg = ArchivedDataPopup(True if self.TableTitleLeft.text() == "Predictions for next year" else False)
        dlg.exec()
        if(dlg.accepted):
                #if seeing predictions checked, load predictions for next year, else load selected archived data
                if(dlg.usePred.isChecked()):
                    #load predictions result
                    self.TableTitleLeft.setText("Predictions for next year")
                else:
                    #load archived data that was selected
                    self.loadTable(self.table,os.curdir+"\\TrainingData"+"\\"+dlg.in1.currentText()+"\\"+dlg.in2.currentText()+".csv")
                    self.TableTitleLeft.setText(dlg.in1.currentText()+ " " + dlg.in2.currentText())


            
    #read table into GUI table viewer
    def loadTable(self, table, file):
        with open(file ,encoding="utf-8") as csvFile:
            csvReader = csv.reader(csvFile)
            data =  list(csvReader)

            rowData = list(data)
            table.setRowCount(len(data))
            table.setColumnCount(len(rowData[0]))
            #offset is so table doesn't have an empty space
            offset = 0
            #for each row in the csv
            for rowIdx, rowData in enumerate(data):
                #Rk sometimes appears in the data, it's a repeat of the header so skip
                if(rowData[0]=="Rk" and rowIdx !=0):
                    offset+=1
                    continue
                #for each data cell in a row
                for colIdx, colData in enumerate(rowData):
                    table.setItem(rowIdx-offset,colIdx,QtWidgets.QTableWidgetItem(colData))
            table.resizeColumnsToContents()  
    
    #update variable with what is in the file
    def readScoringConfig(self):
        fileReader =  open(".//ScoringConfig.txt" ,encoding="utf-8")
        #we only want the number, each value is in a predefined order
        self.RushingReceivingTD = fileReader.readline().split('=')[1]
        self.RushingReceivingYD = fileReader.readline().split('=')[1]
        self.PassingTD = fileReader.readline().split('=')[1]
        self.PPR = fileReader.readline().split('=')[1]
        self.Interceptions = fileReader.readline().split('=')[1]
        self.PassingYd = fileReader.readline().split('=')[1]
        fileReader.close()

    def writeScoringConfig(self,RushingReceivingTD,RushingReceivingYD,PassingTD,PPR,Interceptions,PassingYd):
        fileWriter =  open(".//ScoringConfig.txt" ,encoding="utf-8",mode='w')
        #write the values in the predefined order
        fileWriter.write("Rushing/ReceivingTD="+str(RushingReceivingTD)+"\n")
        fileWriter.write("Rushing/ReceivingYDs="+str(RushingReceivingYD)+"\n")
        fileWriter.write("PassingTD="+str(PassingTD)+"\n")
        fileWriter.write("PointPerReception="+str(PPR)+"\n")
        fileWriter.write("PassingInterceptionsThrown="+str(Interceptions)+"\n")
        fileWriter.write("Passing Yard="+str(PassingYd))
        fileWriter.flush()
        fileWriter.close()      

class ArchivedDataPopup(QtWidgets.QDialog):

    def __init__(self,UsePred):
        super().__init__()

        #setup basic modal stuff
        QBtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        #title
        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Select year and data you want to view")
        
        #year combobox setup
        self.enter1 =  QtWidgets.QHBoxLayout()
        self.txt1 = QtWidgets.QLabel("Year: ")
        self.in1 = QtWidgets.QComboBox()
        #dynamically add training data because we get new data each year
        self.in1.addItems( os.listdir(os.curdir+"\\TrainingData"))
        #add label and combobox to a layout so they're on the same level
        self.enter1.addWidget(self.txt1)
        self.enter1.addWidget(self.in1)

        #dataset combobox setup
        self.enter2 =  QtWidgets.QHBoxLayout()
        self.txt2 = QtWidgets.QLabel("Data set: ")
        self.in2 = QtWidgets.QComboBox()
        #these are the only data types we have and will ever have, so it's hardcoded
        self.in2.addItems(["passing","reveiving","rushing"])
        #add label and combobox to a layout so they're on the same level
        self.enter2.addWidget(self.txt2)
        self.enter2.addWidget(self.in2)

        #setup radio buttons, PySide automatically groups them
        self.usePred = QtWidgets.QRadioButton("Display predictions for next year", self)
        self.useArchived = QtWidgets.QRadioButton("Display archived data", self)
        #preselect a button based on current settings
        if(UsePred):
            self.usePred.setChecked(True)
        else:
            self.useArchived.setChecked(True)

        #add everything to the popup
        self.layout.addWidget(message)
        self.layout.addLayout(self.enter1)
        self.layout.addLayout(self.enter2)
        self.layout.addWidget(self.usePred,alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.useArchived,alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.buttonBox,alignment=QtCore.Qt.AlignCenter)
        
        self.setLayout(self.layout)


class ModifiersPopup(QtWidgets.QDialog):
    def __init__(self,RRTD,RRYD,PTD,PPR,I,PY):
        super().__init__()

        #setup basic modal stuff
        self.setWindowTitle("Point Modifiers")

        QBtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Enter the point modifiers for your league:")

        #input mask docs
        #https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QLineEdit.html#PySide6.QtWidgets.PySide6.QtWidgets.QLineEdit.inputMask

        self.enter1 =  QtWidgets.QHBoxLayout()
        self.txt1 = QtWidgets.QLabel("Rushing/Receiving TD: ")
        self.in1 = QtWidgets.QLineEdit()
        #set input mask so user can't enter strings to numerical settings
        self.in1.setInputMask("00")
        #preset text field to what is already loaded
        self.in1.setText(str(RRTD))
        self.enter1.addWidget(self.txt1)
        self.enter1.addWidget(self.in1,alignment=QtCore.Qt.AlignRight)

        self.enter2 =  QtWidgets.QHBoxLayout()
        self.txt2 = QtWidgets.QLabel("Rushing/Receiving YD's: ")
        self.in2 = QtWidgets.QLineEdit()
        self.in2.setInputMask("00")
        self.in2.setText(str(RRYD))
        self.enter2.addWidget(self.txt2)
        self.enter2.addWidget(self.in2,alignment=QtCore.Qt.AlignRight)

        self.enter3 =  QtWidgets.QHBoxLayout()
        self.txt3 = QtWidgets.QLabel("Passing TD: ")
        self.in3 = QtWidgets.QLineEdit()
        self.in3.setInputMask("00")
        self.in3.setText(str(PTD))
        self.enter3.addWidget(self.txt3)
        self.enter3.addWidget(self.in3,alignment=QtCore.Qt.AlignRight)

        self.enter4 =  QtWidgets.QHBoxLayout()
        self.txt4 = QtWidgets.QLabel("Points Per Reception: ")
        self.in4 = QtWidgets.QLineEdit()
        self.in4.setInputMask("0.00")
        self.in4.setText(str(PPR))
        self.enter4.addWidget(self.txt4)
        self.enter4.addWidget(self.in4,alignment=QtCore.Qt.AlignRight)

        self.enter5 =  QtWidgets.QHBoxLayout()
        self.txt5 = QtWidgets.QLabel("Interceptions: ")
        self.in5 = QtWidgets.QLineEdit()
        self.in5.setInputMask("-00")
        self.in5.setText(str(I))
        self.enter5.addWidget(self.txt5)
        self.enter5.addWidget(self.in5,alignment=QtCore.Qt.AlignRight)

        self.enter6 =  QtWidgets.QHBoxLayout()
        self.txt6 = QtWidgets.QLabel("Passing yards: ")
        self.in6 = QtWidgets.QLineEdit()
        self.in6.setInputMask("0.00")
        self.in6.setText(str(PY))
        self.enter6.addWidget(self.txt6)
        self.enter6.addWidget(self.in6,alignment=QtCore.Qt.AlignRight)

        self.layout.addWidget(message)
        self.layout.addLayout(self.enter1)
        self.layout.addLayout(self.enter2)
        self.layout.addLayout(self.enter3)
        self.layout.addLayout(self.enter4)
        self.layout.addLayout(self.enter5)
        self.layout.addLayout(self.enter6)

        self.layout.addWidget(self.buttonBox,alignment=QtCore.Qt.AlignCenter)
        self.setLayout(self.layout)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.setMinimumSize(800,600)
    widget.showMaximized()
    
    sys.exit(app.exec())