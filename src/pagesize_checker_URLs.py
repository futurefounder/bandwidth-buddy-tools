import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from tqdm import tqdm
from datetime import datetime
import os
import re  # Import regex module for URL validation

# Regex pattern to validate URL
URL_PATTERN = re.compile(r'^https?://[^\s/$.?#].[^\s]*$')

def get_asset_size(url):
    """
    Get the size of an asset in kilobytes (KB) by sending a HEAD request to the URL.
    """
    try:
        response = requests.head(url, allow_redirects=True)
        size = int(response.headers.get('content-length', 0)) / 1024  # Convert bytes to KB
        return size
    except Exception as e:
        print(f"Error fetching size for {url}: {e}")
        return 0

def find_assets(url, size_threshold):
    """
    Extract and calculate the size of all assets (images, scripts, links, videos) on a webpage.
    """
    print(f"Processing URL: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    assets = []
    tags = {
        'img': 'src',
        'script': 'src',
        'link': 'href',
        'video': 'src',
        'source': 'src'  
    }
    
    for tag, attr in tags.items():
        for element in soup.find_all(tag):
            asset_url = element.get(attr)
            if asset_url:
                full_url = urljoin(url, asset_url)
                size = get_asset_size(full_url)
                if size >= size_threshold:  # Only record assets above the threshold
                    assets.append((full_url, size))
                    print(f"Found asset: {full_url} with size {size:.2f} KB")
    
    return assets

def main(urls, output_option, size_threshold):
    """
    Main function that processes a list of URLs, finds large assets, and outputs results.
    """
    all_assets = []
    
    for url in tqdm(urls, desc="Processing pages"):
        assets = find_assets(url, size_threshold)
        for asset in assets:
            all_assets.append((url, asset[0], asset[1]))
    
    if output_option == 'console':
        # Print results to console
        print("Page URL | Asset URL | Size (KB)")
        print("-" * 100)
        for page_url, asset_url, size in all_assets:
            print(f"{page_url} | {asset_url} | {size:.2f} kB")
    elif output_option == 'file':
        # Save results to a CSV file in the outputs folder
        outputs_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'outputs'))
        os.makedirs(outputs_folder, exist_ok=True)  # Create outputs folder if it doesn't exist
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_csv = os.path.join(outputs_folder, f'large_assets_{timestamp}.csv')
        df = pd.DataFrame(all_assets, columns=['Page URL', 'Asset URL', 'Size (KB)'])
        df.to_csv(output_csv, index=False)
        print(f"Results saved to {output_csv}")

def validate_urls(urls):
    """
    Validate that all URLs follow the correct format. Returns True if all are valid, False otherwise.
    """
    for url in urls:
        if not re.match(URL_PATTERN, url):
            return False
    return True

# Prompt the user for input
while True:
    output_choice = input("Do you want the results in the console or as a file? (press 'c' for console, 'f' for file, 'x' to exit): ").strip().lower()
    if output_choice == 'c':
        output_option = 'console'
        break
    elif output_choice == 'f':
        output_option = 'file'
        break
    elif output_choice == 'x':
        print("Exiting the script.")
        exit()
    else:
        print("Invalid choice. Please press 'c' for console, 'f' for file, or 'x' to exit.")

# Loop to get valid URLs from the user
while True:
    urls_input = input("Enter a comma-separated list of URLs (e.g., https://example.com/page1, https://example.com/page2, https://example.com/page3): ").strip()
    urls_to_check = [url.strip() for url in urls_input.split(',')]
    
    # Validate URLs
    if validate_urls(urls_to_check):
        break
    else:
        print("Error: One or more URLs are invalid. Please enter valid URLs starting with 'http://' or 'https://'.")

# Prompt for the size threshold
while True:
    try:
        size_threshold = float(input("Enter the size threshold in kilobytes (KB) for reporting large assets (recommendation 100): ").strip())
        break
    except ValueError:
        print("Error: Please enter a valid number for the size threshold.")

# Call the main function with the provided arguments
main(urls_to_check, output_option, size_threshold)
