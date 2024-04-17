#Using Python 3.12.2 64-bit
import os,csv,pathlib

class Algorithm:
    # def __init__(self) -> None:
    #     pass
    
    def read_csv():
        year = 2003
        root = "c:\\Users\\ei5252ec\\git\\Fantasy-Football-Assistant\\"
        for folder in os.listdir(root):
            if year == 2024:
                break
            for file in os.listdir(root+"/"+folder):
                if(file.endswith(".csv")):
                    print(root+"/"+folder+"/"+file)
                    with open(root+"\\"+str(year)+"\\"+file, 'r') as csvfile:
                        reader = csv.reader(csvfile)
                        for row in reader:
                            print(row)                
            year+= 1
            #train or something idk
        return 1

if __name__ == "__main__":
   Algorithm.read_csv()
   print("done")