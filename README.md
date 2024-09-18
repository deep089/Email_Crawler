# Email_Crawler_Script
This Script Scrapes Email from Website pages
This project is a Python-based web crawler designed to extract email addresses from a list of websites. It uses the `requests`, `BeautifulSoup`, and `concurrent.futures` libraries to efficiently scrape and process multiple websites concurrently.

## Features

- Extracts email addresses from web pages.
- Crawls multiple websites concurrently.
- Custom headers to mimic a web browser.
- Filters out invalid URLs and non-HTML content.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

You can install the required libraries using pip:

```bash
pip install requests beautifulsoup4
```

## Usage

1. Clone the repository:

```bash
https://github.com/deep089/Email_Crawler.git
cd email-crawler
```

2. Update the `start_urls` list in the `main` section of the script with the URLs you want to crawl.

3. Run the script:

```bash
python email_crawler.py
```

## Code Overview

### `extract_emails_from_url(url)`

This function takes a URL as input, sends a GET request to the URL, and uses a regular expression to find and return a set of email addresses found in the page content.

### `is_valid_url(url, base_url)`

This function checks if a URL is valid for crawling. It ensures the URL starts with '/' or the base URL and excludes links to images, PDFs, and other non-HTML content.

### `crawl_website(start_url)`

This function crawls a single website starting from the given URL. It extracts email addresses and finds new links to crawl, ensuring no URL is visited more than once.

### `crawl_multiple_websites(start_urls)`

This function takes a list of starting URLs and uses a thread pool to crawl multiple websites concurrently. It aggregates email addresses found across all websites.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

