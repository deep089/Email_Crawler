# -*- coding: utf-8 -*-
"""Email_Scraper.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1s50fejwUfLLk0WTd4UfAIb0RsEdT1sOi
"""

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import concurrent.futures

# Custom headers to mimic a web browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def extract_emails_from_url(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        emails = set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', soup.text))
        return emails
    except requests.exceptions.RequestException:
        return set()

def is_valid_url(url, base_url):
    # Exclude URLs that don't start with '/' or base_url and exclude image/pdf links
    return (url.startswith('/') or url.startswith(base_url)) and not urlparse(url).path.endswith(('.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx', '.xls', '.xlsx'))

def crawl_website(start_url):
    visited_urls = set()
    emails_set = set()
    urls_to_visit = [start_url]

    while urls_to_visit:
        current_url = urls_to_visit.pop(0)
        if current_url not in visited_urls:
            visited_urls.add(current_url)
            new_emails = extract_emails_from_url(current_url)
            emails_set.update(new_emails)

            # Find all links on the current page
            try:
                response = requests.get(current_url, headers=headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                base_url = "{0.scheme}://{0.netloc}".format(urlparse(current_url))
                for link in soup.find_all('a', href=True):
                    new_url = urljoin(base_url, link['href'])
                    if is_valid_url(new_url, base_url) and new_url not in visited_urls:
                        urls_to_visit.append(new_url)
            except requests.exceptions.RequestException:
                continue

    return emails_set

def crawl_multiple_websites(start_urls):
    all_emails = set()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(crawl_website, url): url for url in start_urls}
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                emails_set = future.result()
                all_emails.update(emails_set)
            except Exception as e:
                print(f"Exception occurred: {e}")
    return all_emails

if __name__ == "__main__":
    start_urls = [

        'https://www.santopseal.com'  # Add more URLs as needed

    ]
    emails_set = crawl_multiple_websites(start_urls)
    for email in emails_set:
        print(email)