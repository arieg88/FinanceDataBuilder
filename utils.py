import time
import random
import ast
import os
import json

# List of top companies in the S&P 500
SP_TOP = ['Apple', 'Microsoft', 'Nvidia', 'Amazon', 'Meta', 'Alphabet', 'Berkshire Hathaway', 'Broadcom', 'Eli Lilly', 'Jpmorgan', 'Tesla'] 

# Mapping of company names to their respective stock tickers
tickers = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Nvidia': 'NVDA',
    'Amazon': 'AMZN',
    'Meta': 'META',
    'Alphabet': 'GOOGL',
    # 'Alphabet_Class_C': 'GOOG',
    'Berkshire_Hathaway': 'BRK.A',
    # 'Berkshire_Hathaway_Class_B': 'BRK.B',
    'Broadcom': 'AVGO',
    'Eli_Lilly': 'LLY',
    'JPMorgan': 'JPM',
    'Tesla': 'TSLA'
}

def read_headers():
    """Read headers and cookies from text files and parse them to dictionaries.

    Returns:
        tuple: A tuple containing headers and cookies dictionaries.
    """
    # Read headers from the file
    with open('./assets/headers.txt', 'r') as file:
        headers = ast.literal_eval(file.read())
    
    # Read cookies from the file
    with open('./assets/cookies.txt', 'r') as file:
        cookies = ast.literal_eval(file.read())

    return headers, cookies

def random_sleep(sleep_times=[2, 3, 4, 5, 6]):
    """Pause the program for a random duration chosen from sleep_times.

    Args:
        sleep_times (list): A list of possible sleep durations in seconds.
    """
    time.sleep(random.choice(sleep_times))

def try_again_or_continue(url, next_data='month'):
    """Prompt the user to retry or continue to the next data item after a failure.

    Args:
        url (str): The URL that failed to load.
        next_data (str): The type of data to move to if the user opts to continue.
    
    Returns:
        bool: True if the user chooses to retry, False to continue.
    """
    print(f'Failed with {url}')
    inp = input(f'Enter 1 to Try again, or Enter 2 to continue to the next {next_data}:\n')
    
    # Evaluate user input to determine next action
    if inp == '1':
        return True
    elif inp == '2':
        return False
    else:
        print('Invalid input, assuming retry.')
        return True
    
def save_articles(articles, company, month, year=2024):
    """Save a list of article dictionaries to a JSON file.

    Args:
        articles (list): A list of dictionaries containing article details.
        company (str): The name of the company for which articles are saved.
        month (int): The month of the articles being saved.
        year (int): The year of the articles being saved (default is 2024).
    
    Returns:
        bool: True if articles are saved successfully, False otherwise.
    """
    try:
        # Ensure the company and year directory exists
        os.makedirs(f'./articles/{company}/{year}', exist_ok=True)
        
        # Write articles to a JSON file for the specified month and year
        with open(f'./articles/{company}/{year}/{month}_articles.json', 'w') as json_file:
            json.dump(articles, json_file, indent=4)
        
        return True
    except Exception as e:
        print(f'Error saving articles: {e}')  # Log error if saving fails
        return False  # Indicate failure if saving is unsuccessful
