from django.shortcuts import render
from django.http import HttpResponse
import os, csv

def loadTable(file):
    with open(file, "r") as f:
        print("Here")
        reader = csv.reader(f)
        header = next(reader)  # Get the header row.
        rows = []
        for row in reader:
            print(row)
            rows.append(row)
        return header, rows
# Create your views here.
def home(request):
        # Example dynamic data for table1 and table2
    temp = loadTable("../gen_rankings.csv")
    table1_data = {
        "headers": temp[0],
        "rows": temp[1]
        
    }
    temp = loadTable("../ranking-table.csv")
    table2_data = {
        "headers": temp[0],
        "rows": temp[1]
    }
    
    context = {
        'table1': table1_data,
        'table2': table2_data
    }

    return render(request, r'home.html', context)

