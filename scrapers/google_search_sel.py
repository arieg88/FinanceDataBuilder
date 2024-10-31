import time
import random
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
from pathlib import Path
import sys
# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import *

def get_urls(soup, site_url):
    """
    Extract URLs from the provided BeautifulSoup object based on the specified site URL.

    Args:
        soup (BeautifulSoup): Parsed HTML page source.
        site_url (str): Base URL of the site to filter links.

    Returns:
        list: A list of URLs containing the specified site URL.
    """
    urls = []
    for link in soup.find_all('a'):
        try:
            url = link.get('href')  # Safely get the href attribute
            if url and site_url in url:
                urls.append(url)
        except Exception as e:
            print(f"Error parsing link: {e}")
    return urls

def get_queries(entity, site, year):
    """
    Generate search queries for each month for a given entity and year.

    Args:
        entity (str): Name of the entity.
        site (str): Site domain to limit the search.
        year (int): Year of interest for the search.

    Returns:
        list: A list of tuples containing query strings for each month and the month number.
    """
    # Queries for January to November
    queries = [(f"intitle:{entity}+site:{site}+after:{year:04d}/{month:02d}/01+before:{year:04d}/{month+1:02d}/01", month) for month in range(1, 12)]
    # Query for December
    queries.append((f"intitle:{entity}+site:{site}+after:{year:04d}/12/01+before:{(year+1):04d}/01/01", 12))
    return queries

def get_monthly_dict(queries, entity, year, site_url, driver):
    """
    Retrieve and save URLs for each month based on the provided search queries.

    Args:
        queries (list): List of query strings and respective month numbers.
        entity (str): Name of the entity for organizing directory structure.
        year (int): Year of the search to save URLs by date.
        site_url (str): URL filter to include only links from this base URL.

    Returns:
        dict: A dictionary with month numbers as keys and lists of URLs as values.
    """
    monthly_dict = {}
    for query, month in queries:
        print(f'Searching for month: {month}')
        url = 'https://www.google.com/search?q=' + query
        urls = []
        start = 0
        urls_len = 0

        # Paginate through Google search results
        while True:
            if start > 0:
                url = f'https://www.google.com/search?q={query}&start={start}'

            driver.get(url)  # Open URL with Selenium
            random_sleep()  # Random sleep to avoid detection

            # Parse page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # If parsing fails, print raw HTML and exit loop
            if soup is None:
                print("Failed to parse the page.")
                print(driver.page_source)  # Raw HTML for debugging
                break

            # Extract URLs from the page
            urls += get_urls(soup, site_url)

            # Check if no new URLs were added, signaling end of results for the month
            if urls_len == len(urls):  
                all_ul = soup.find_all('ul')
                if len(all_ul[1].find_all('li')) == 4:
                    print(f'Done with {month} (moving to next month)')
                    break
                
                if try_again_or_continue(url):
                    headers, cookies = read_headers()
                    continue
                else:
                    print(f'Done with {month} (moving to next month)')
                    break

            # Update count of collected URLs and increment start for pagination
            urls_len = len(urls)
            start += 10  # Move to next page of results

        monthly_dict[month] = urls

    # Ensure the directory exists for saving URLs by month
    Path(f'../urls/{entity}/{year}').mkdir(parents=True, exist_ok=True)

    # Save URLs for the current month
    with open(Path(f'../urls/{entity}/{year}/{month}_urls.txt'), 'w') as file:
        file.write(str(urls))


    return monthly_dict

def main(site_url, year, site, entities):
    """
    Main function to initialize the Selenium driver, load headers and cookies,
    and scrape URLs for specified entities across different months.
    """
    # Set up Chrome options for headless browsing (optional)
    chrome_options = Options()
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the WebDriver (ensure chromedriver is in PATH or specify Service path)
    driver = webdriver.Chrome(options=chrome_options)

    # Load headers and cookies for requests
    headers, cookies = read_headers()

    # Loop through entities and generate URLs for each
    for entity in entities: 
        queries = get_queries(entity, site, year) 
        monthly_dict = get_monthly_dict(queries, entity, year, site_url, driver) 

    # Close the Selenium WebDriver after scraping
    driver.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape Yahoo Finance URLs for specified entities.')
    parser.add_argument('site_url', type=str, help='Base URL of the site to scrape (e.g., https://finance.yahoo.com/)')
    parser.add_argument('year', type=int, help='Year of interest for the search (e.g., 2024)')
    parser.add_argument('site', type=str, help='Site domain to limit the search (e.g., finance.yahoo.com)')
    parser.add_argument('entities', nargs='+', help='List of entities to search for (e.g., Company1 Company2 ...)')

    args = parser.parse_args()

    main(args.site_url, args.year, args.site, args.entities)
