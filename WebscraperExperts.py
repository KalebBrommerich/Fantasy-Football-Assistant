from bs4 import BeautifulSoup
import requests
import os,pathlib
import pandas as pd
import numpy as np
"""
Class is used to webscrape the expert consensus page at fantasypros 
"""
class WebscraperExperts:

    def __init__(self, url, id):
        self.url = url
        self.table_id = id

    def get_html_content(self):
        response = requests.get(self.url)
        print(self.url)
        return response.content

    def get_table(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table', id=self.table_id)
        #print(table)
        return table
        
    def get_headers(self, table):
        header_rows = table.find('thead').find('tr').find_all('th')
        headerNum = 0
        unparsedHeaders = []
        for row in header_rows:
            headerNum+=1
            if(headerNum <=2 ):
                unparsedHeaders.append(row.get_text().strip())
                continue
            unparsedHeaders.append(row.find('span').get_text())
        headerNum = 0
        parsedHeaders = []
        for header in unparsedHeaders:
            headerNum+=1
            if(headerNum <=2 ):
                parsedHeaders.append(header.lower().capitalize())
                continue
            nameOnly = header.split()[0] +" "+ header.split()[1]
            parsedHeaders.append(nameOnly)
        #print(parsedHeaders)
        return parsedHeaders


    def get_rows(self, table):
        rows = []
        #rows.append()
        for row in table.find('tbody').find_all('tr'):
            cols = []
            colNum = 0
            for ele in row.find_all(['td']):
                colNum +=1
                if colNum == 2:
                    cols.append(ele.find(class_="everything-but-mobile js-sort-field").get_text().strip())
                else:
                    cols.append(ele.get_text().strip())
            rows.append(cols)
        return rows

    def get_dataframe(self, headers, rows):
        df = pd.DataFrame(rows, columns=headers)
        return df
    
    def scrape_table_to_csv(self, table_id, csv_file_path='table_data.csv'):
        html_content = self.get_html_content()
        table = self.get_table(html_content)
        #the print slows it down a lot, if it's not slowed your traffic will be blocked for an hour if you scrape the past 20 years
        headers = self.get_headers(table)
        rows = self.get_rows(table)
        df = self.get_dataframe(headers, rows)
        if not os.path.exists(str(pathlib.Path.cwd())+"\\"+csv_file_path.split('\\')[0]):
            os.mkdir(str(pathlib.Path.cwd())+"\\"+csv_file_path.split('\\')[0])
        df.to_csv(csv_file_path, index=False)
        print(f"Data saved to {csv_file_path}")

def main(url, id):
    # Initialize the Webscraper with the URL - this will be used to get the HTML content
    scraper = WebscraperExperts(url,id)

    # Get HTML content - this will be used to extract the table
    html_content = scraper.get_html_content()

    # Extract table from the HTML content - this will be used to create a DataFrame
    table = scraper.get_table(html_content)

    # Get headers and rows from the table - these will be used to create a DataFrame
    headers = scraper.get_headers(table)
    rows = scraper.get_rows(table)

    # # Convert to DataFrame - pandas is used to convert the data to a DataFrame
    df = scraper.get_dataframe(headers, rows)

    # # Save the DataFrame to a CSV file
    csv_file_path = id+'.csv'
    df.to_csv(csv_file_path, index=False)
    print(f"Data saved to {csv_file_path}")
    print("done")

if __name__ == "__main__":
    #Example URL - replace with the actual URL you intend to scrape
    url = "https://www.fantasypros.com/nfl/fantasy-football-rankings.php"
    id = "ranking-table"
    main(url,id)
