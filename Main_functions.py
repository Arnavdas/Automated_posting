

from bs4 import BeautifulSoup
import requests

def scrape_web_page(url = 'https://odishatv.in/odisha/bhubaneswar'):
    # url+='/15' # For next page

    try:
        # Send a request to the url main page
        # Adding a user agent to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)

        # Raise an exception for bad status codes
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract different sections from the main page
        results = {}

        return results, soup

    except requests.RequestException as e:
        print(f"Error occurred while scraping: {e}")
        return None, None
