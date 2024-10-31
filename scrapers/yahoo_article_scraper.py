import ast
import requests
from bs4 import BeautifulSoup
import json
import sys
import os
# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import *


def save_articles(articles, entity, month, year):
    """Save the list of article dictionaries to a JSON file.

    Args:
        articles (list): A list of dictionaries containing article details.
        entity (str): The name of the entity (company or other) for which articles are saved.
        month (int): The month of the articles being saved.
        year (int): The year of the articles being saved.
    
    Returns:
        bool: True if articles are saved successfully, otherwise False.
    """
    try:
        # Ensure the year directory exists
        os.makedirs(f'../articles/{entity}/{year}', exist_ok=True)
        
        # Write the articles to a JSON file
        with open(f'../articles/{entity}/{year}/{month}_articles.json', 'w') as json_file:
            json.dump(articles, json_file, indent=4)
        
        return True
    except Exception as e:
        print(f'Error saving articles: {e}')  # Log the error if saving fails
        return False

def scrape_yahoo_finance(urls, headers, cookies):
    """Scrape articles from Yahoo Finance given a list of URLs.

    Args:
        urls (list): A list of URLs to scrape articles from.
        headers (dict): Headers to include in the GET request.
        cookies (dict): Cookies to include in the GET request.
        autosave (bool): If True, articles will be saved automatically after scraping.
    
    Returns:
        list: A list of dictionaries containing scraped articles.
    """
    articles = []

    # Iterate through the provided URLs
    for url in urls:
        random_sleep([1, 2])  # Sleep to avoid being rate-limited
        scraped = False
        
        # Attempt to scrape the article until successful
        while not scraped:
            try:
                # Send GET request to the article URL
                response = requests.get(url, cookies=cookies, headers=headers)
                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract article details
                title = soup.find('h1', class_='cover-title').text  # Extract article title
                author = soup.find('div', class_='byline-attr-author').text  # Extract author name
                date = soup.find('time').get('data-timestamp')  # Extract publication date
                
                # Extract the article text
                text = ''
                for p in soup.find('div', class_='body').find_all('p'):
                    text += p.text + '\n'
                
                # Append the article data to the articles list
                articles.append({
                    'Date': date,
                    'Title': title,
                    'Author': author,
                    'Text': text
                })
                
                scraped = True
                print(f'Finished scraping article in {url}')

            except Exception as e:
                print(f'Error scraping {url}: {e}')  # Log the error if scraping fails
                new_headers = try_again_or_continue(url, 'article')
                if new_headers:
                    headers, cookies = read_headers()  # Refresh headers and cookies if necessary
                else:
                    scraped = True  # Stop trying if unable to get new headers

    return articles

def main(site_url, year, site, entities):
    """Main function to scrape articles from Yahoo Finance for specified entities.

    Args:
        site_url (str): The base URL of the site to scrape articles from.
        year (int): The year to filter articles.
        site (str): The site domain to limit the search.
        entities (list): A list of entities (companies or other) to scrape articles for.
    """
    # Read headers and cookies for HTTP requests
    headers, cookies = read_headers()

    # Iterate through entities and months to scrape articles
    for entity in entities:  # Loop through each specified entity
        for month in range(1, 13):  # Loop through each month
            # Construct the file path for the URL file
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'urls'))
            file_path = os.path.join(base_dir, entity, str(year), f"{month}_urls.txt")

            # Check if the file exists before attempting to open it
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}. Skipping this month.")
                continue  # Skip to the next month if the file doesn't exist

            # Load the list of URLs from the file
            with open(file_path, 'r') as file:
                urls = ast.literal_eval(file.read())  # Evaluate the string to a list
            
            articles = scrape_yahoo_finance(urls, headers, cookies)  # Scrape the articles from the URLs
            save_articles(articles, entity, month, year)  # Save articles if autosave is enabled
            
            print(f'Finished scraping articles from Yahoo Finance in {month}/{year}')

if __name__ == '__main__':
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) < 5:
        print("Usage: python script_name.py <site_url> <year> <site> <entity1> [<entity2> ...]")
        print("Example: python script_name.py 'https://finance.yahoo.com' 2024 'yahoo' 'Apple' 'Microsoft'")
        sys.exit(1)  # Exit the program with an error code

    # Extract command-line arguments
    site_url = sys.argv[1]
    year = int(sys.argv[2])
    site = sys.argv[3]
    entities = sys.argv[4:]  # The remaining arguments are treated as entities

    main(site_url, year, site, entities)  # Call the main function with provided arguments
