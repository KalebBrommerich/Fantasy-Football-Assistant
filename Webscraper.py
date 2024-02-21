#Using Python 3.12.2 64-bit
from bs4 import BeautifulSoup
import requests
import csv
#pip install beautifulsoup4
#pip install requests
#pip install csv
#https://beautiful-soup-4.readthedocs.io/en/latest/index.html?highlight=download
class Webscraper:
    def __init__(self, url: str, table_id: str) -> None:
        self.url = url
        self.table_id = table_id

    def scrape_table(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        response = requests.get(self.url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', id=self.table_id)

            headers = [th.text for th in table.find('thead').find_all('th')]
            rows = table.find('tbody').find_all('tr')

            table_data = [headers]

            for row in rows:
                row_header = row.find('th')
                if row_header:
                    row_data = [row_header.text.strip()]
                else:
                    row_data = []

                cells = row.find_all('td')
                row_data += [cell.text.strip() for cell in cells]

                if len(row_data) > 1:
                    table_data.append(row_data)

            with open('table_data.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(table_data)
        else:
            print(f"Failed to retrieve data: HTTP {response.status_code}")