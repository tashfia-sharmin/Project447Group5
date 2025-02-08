import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

def convert_to_uni(word):
    return [ord(char) for char in word]

def scrape_word_frequency(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        script_content = soup.find('td', class_='scrtext').get_text(separator=" ", strip=True)
        words = re.findall(r'\b\w+\b', script_content.lower())
        uni_word_frequency = Counter(tuple(convert_to_uni(word)) for word in words)

        return uni_word_frequency

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {}
    except AttributeError:
        print("Error: Unable to find the script content on the page.")
        return {}

url = "https://imsdb.com/scripts/Interstellar.html"
word_frequency = scrape_word_frequency(url)
