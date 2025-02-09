import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

def convert_to_uni(word):
    return [ord(char) for char in word]

def scrape_word_frequency_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")

        # Extract text from each `<p class="subtitle">`
        subtitles = [p.get_text(strip=True) for p in soup.find_all("p", class_="subtitle")]

        word_frequency = Counter()
        uni_word_frequency = Counter()

        for subtitle in subtitles:
            subtitle = subtitle.replace('�', '')
            subtitle = subtitle.replace('-', '')
            words = re.findall(r'\b\w+\b', subtitle.lower())
            word_frequency.update(words)
            uni_word_frequency.update(convert_to_uni(word) for word in words)

        return uni_word_frequency

    except Exception as e:
        print(f"Error: {e}")
        return None, None

# TEST
# word_freq = scrape_word_frequency_from_file("output2.html")
# print(word_freq.most_common(10))  # Print the 10 most common words


# OLD
# def scrape_word_frequency(url):
#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)

#         # Parse the HTML content
#         soup = BeautifulSoup(response.text, 'html.parser')

#         script_content = soup.find('td', class_='scrtext').get_text(separator=" ", strip=True)
#         words = re.findall(r'\b\w+\b', script_content.lower())
#         uni_word_frequency = Counter(tuple(convert_to_uni(word)) for word in words)

#         return uni_word_frequency

#     except requests.exceptions.RequestException as e:
#         print(f"Error: {e}")
#         return {}
#     except AttributeError:
#         print("Error: Unable to find the script content on the page.")
#         return {}

# url = "https://imsdb.com/scripts/Interstellar.html"
# word_frequency = scrape_word_frequency(url)
