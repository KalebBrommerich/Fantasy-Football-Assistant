from bs4 import BeautifulSoup
import requests
import pandas as pd

class Webscraper:

    def __init__(self, url, id):
        self.url = url
        self.table_id = id

    def get_html_content(self):
        response = requests.get(self.url)
        return response.content

    def get_table(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table', id=self.table_id)
        #print(table)
        return table
        
    def get_headers(self, table):
        header_rows = table.find('thead').find_all('tr')
        # Assume the last row of headers is the one that directly corresponds to data columns - this fixes the 2 layered header issue 
        final_header_row = header_rows[-1]
        headers = [header.text for header in final_header_row.find_all('th')]
        return headers


    def get_rows(self, table):
        rows = []
        for row in table.find('tbody').find_all('tr'):
            cols = [ele.text.strip() for ele in row.find_all(['th','td'])]
            rows.append(cols)
        return rows

    def get_dataframe(self, headers, rows):
        df = pd.DataFrame(rows, columns=headers)
        return df
    
    def scrape_table_to_csv(self, table_id, csv_file_path='table_data.csv'):
        html_content = self.get_html_content()
        table = self.get_table(html_content)
        headers = self.get_headers(table)
        rows = self.get_rows(table)
        df = self.get_dataframe(headers, rows)
        df.to_csv(csv_file_path, index=False)
        print(f"Data saved to {csv_file_path}")

def main(url, id):
    # Initialize the Webscraper with the URL - this will be used to get the HTML content
    scraper = Webscraper(url,id)

    # Get HTML content - this will be used to extract the table
    html_content = scraper.get_html_content()

    # Extract table from the HTML content - this will be used to create a DataFrame
    table = scraper.get_table(html_content, id)

    # Get headers and rows from the table - these will be used to create a DataFrame
    headers = scraper.get_headers(table)
    rows = scraper.get_rows(table)

    # Convert to DataFrame - pandas is used to convert the data to a DataFrame
    df = scraper.get_dataframe(headers, rows)

    # Save the DataFrame to a CSV file
    csv_file_path = id+'.csv'
    df.to_csv(csv_file_path, index=False)
    print(f"Data saved to {csv_file_path}")

if __name__ == "__main__":
    # Example URL - replace with the actual URL you intend to scrape
    # url = "https://www.pro-football-reference.com/years/2023/passing.htm"
    # id = "passing"
    # url = "https://www.pro-football-reference.com/years/2023/rushing.htm"
    # id = "rushing"
    # url = "https://www.pro-football-reference.com/years/2023/receiving.htm"
    # id = "receiving"
    # url = "https://www.pro-football-reference.com/years/2023/scrimmage.htm"
    # id = "receiving_and_rushing"
    main(url,id)