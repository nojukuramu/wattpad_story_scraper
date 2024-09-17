import requests
from bs4 import BeautifulSoup
import re
import html

def download_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful
        return response.text
    except requests.RequestException as e:
        print(f"Error downloading HTML: {e}")
        return None

def extract_pre_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Replace <br> tags with newline characters
    for br in soup.find_all('br'):
        br.replace_with('\n')

    # Extract text from <pre> tags
    pre_tags = soup.find_all('pre')
    pre_content = '\n'.join(pre.get_text() for pre in pre_tags)  # Join with newlines
    return pre_content

def normalize_symbols(text):
    # Convert HTML entities to their corresponding characters
    text = html.unescape(text)
    # Replace multiple whitespace with a single space
    text = re.sub(r'\s+', ' ', text)
    # Remove non-ASCII characters (if desired, you can remove this line)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    # Remove leading and trailing whitespace
    text = text.strip()
    return text

def main(url):
    html_content = download_html(url)
    if html_content:
        pre_content = extract_pre_content(html_content)
        normalized_content = normalize_symbols(pre_content)
        print(normalized_content)
        with open("output.txt", 'a', encoding='utf-8') as outfile:
            outfile.write(normalized_content + '\n')

    convert_to_lowercase("output.txt")

def process_urls_from_file(filename):
    with open(filename, 'r') as file:
        for line in file:
            url = line.strip()
            if url:  # Check if the line is not empty
                main(url)

def extract_hrefs(input_file):
    # Regular expression to match href attributes
    href_pattern = re.compile(r'href=["\'](http[s]?://[^\s"\']+|/[^"\']*)["\']', re.IGNORECASE)

    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as infile:
        content = infile.read()

    # Find all hrefs
    hrefs = href_pattern.findall(content)

    # Prepend base URL to relative hrefs
    base_url = 'https://www.wattpad.com'
    full_urls = [base_url + href if not href.startswith(('http://', 'https://')) else href for href in hrefs]

    # Write hrefs to the output file
    with open("urls.txt", 'w', encoding='utf-8') as outfile:
        for url in full_urls:
            outfile.write(url + '\n')

def convert_to_lowercase(file_path):
    # Open the file in read mode and read its content
    with open(file_path, 'r') as file:
        content = file.read()

    # Convert all the content to lowercase
    lowercase_content = content.lower()

    # Open the file in write mode and save the modified content
    with open(file_path, 'w') as file:
        file.write(lowercase_content)


if __name__ == "__main__":
    extract_hrefs("input.txt")
    process_urls_from_file('urls.txt')
    