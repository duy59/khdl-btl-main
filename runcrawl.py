import asyncio
from ultis.crawl import crawl_post
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from CrawlDetail.crawldetail import crawl_detail, save_to_csv

async def main():
    base_url = 'https://finance.yahoo.com'
    url = f'{base_url}/lookup/?guccounter=1'
    html_content = await crawl_post(url)
    
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all <a> tags within the <tbody> with class "body yf-1dbt8wv"
    tbody = soup.find('tbody', class_='body yf-1dbt8wv')
    links = tbody.find_all('a', class_='loud-link fin-size-medium yf-1e4diqp')
    
    # Extract the href attribute from each <a> tag and convert to full URL with 'key-statistics' appended
    hrefs = [urljoin(base_url, link.get('href') + 'key-statistics') for link in links]
    
    # Crawl details for each link and save to CSV
    for href in hrefs:
        headers, rows = await crawl_detail(href)
        if headers and rows:
            filename = f'Data/detail_data_{href.split("/")[-2]}.csv'
            save_to_csv(headers, rows, filename)
    
    # Print Done after all crawling is complete
    print("Done")

if __name__ == "__main__":
    asyncio.run(main())