import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import os
import csv

def convert_to_uni(word):
    return tuple(ord(char) for char in word)

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
        return word_frequency

    except Exception as e:
        print(f"Error: {e}")
        return None, None

def process_all_languages(output_file = "data.csv"):
    data = []
    for i in range(38):
        file_path = f"./script_html/lang{i}.html"
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
        word_freq = scrape_word_frequency_from_file(file_path)
        if word_freq:
            for word, freq in word_freq.items():
                #include this if we want to filter out 1 letter words
                # if len(word) > 1:
                uni_word = convert_to_uni(word)
                data.append([word, uni_word, freq, i])
    # Write to CSV file
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Word", "Unicode_Sequence", "Frequency", "Language_ID"])  # Header
        writer.writerows(data)
    print(f"Data saved to {output_file}") 

process_all_languages()
