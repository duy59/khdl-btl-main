import asyncio
import csv
import os
from bs4 import BeautifulSoup
from ultis.crawl import crawl_post

async def crawl_detail(url):
    html_content = await crawl_post(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the table
    table = soup.find('table', class_='table yf-1cqapi1')
    
    if table is None:
        print(f"No table found at {url}")
        return None, None
    
    # Extract headers
    headers = [th.text for th in table.find('thead').find_all('th')]
    
    # Extract rows
    rows = []
    for tr in table.find('tbody').find_all('tr'):
        row = [td.text for td in tr.find_all('td')]
        rows.append(row)
    
    return headers, rows

def save_to_csv(headers, rows, filename='detail_data.csv'):
    if headers is None or rows is None:
        print("No data to save.")
        return
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Write to CSV
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        csvwriter.writerows(rows)