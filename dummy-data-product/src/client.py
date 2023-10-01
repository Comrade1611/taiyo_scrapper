# In[0] Imports

import requests
from bs4 import BeautifulSoup
import csv


# In[1] Scrapping Class

class NASAScraper:
    def __init__(self, url):
        self.url = url

    def pull_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to fetch the page.\n Status code is {response.status_code}")
            return None

    def traverse_data(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        content_div = soup.find('div', class_='markdown-body')  # Locate the content

        data = []
        for header in content_div.find_all(['h2', 'h3']):
            section_title = header.text.strip()
            section_content = header.find_next('p').text.strip()
            data.append((section_title, section_content))

        return data

    def data_to_csv(self, data):
        with open('NASA_API_Info.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Section Title', 'Section Content'])
            writer.writerows(data)

    def run(self):
        html_content = self.pull_data()
        if html_content:
            data = self.traverse_data(html_content)
            self.data_to_csv(data)


# In[2] main

if __name__ == "__main__":
    scraper = NASAScraper('https://www.earthdata.nasa.gov/engage/open-data-services-and-software/api')
    scraper.run()