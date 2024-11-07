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
    soup = BeautifulSoup(html_content, 'html.parser')

# Find the <tbody> with the specified class
    tbody = soup.find('tbody', class_='body yf-paf8n5')
    if tbody:
        links = tbody.find_all('a', class_='loud-link fin-size-medium yf-1e4diqp')
    else:
        print("tbody not found")
        links = []

# Proceed only if links are found
    if links:
        # Extract hrefs and proceed
        hrefs = [urljoin(base_url, link.get('href') + 'key-statistics') for link in links]

        # Crawl details for each link and save to CSV
        for href in hrefs:
            print(f"Crawling {href}")
            headers, rows = await crawl_detail(href)
            if headers and rows:
                filename = f'Data/detail_data_{href.split('/')[-2]}.csv'
                save_to_csv(headers, rows, filename)
    else:
        print("No links found to process.")

        
    # Print Done after all crawling is complete
    print("Done")        

if __name__ == "__main__":
    asyncio.run(main())