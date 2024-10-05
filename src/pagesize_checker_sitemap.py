import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from tqdm import tqdm
from datetime import datetime
import os

# Size threshold in KB for reporting
SIZE_THRESHOLD = 50

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

def find_assets(url):
    """
    Extract and calculate the total size of all assets (images, scripts, links, videos) on a given webpage.
    """
    print(f"Processing URL: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    total_size = 0
    tags = {
        'img': 'src',
        'script': 'src',
        'link': 'href', 
        'video': 'src'
    }
    
    for tag, attr in tags.items():
        for element in soup.find_all(tag):
            asset_url = element.get(attr)
            if asset_url:
                full_url = urljoin(url, asset_url)
                size = get_asset_size(full_url)
                total_size += size
    
    return total_size

def parse_sitemap(sitemap_url):
    """
    Parse the sitemap XML file and return a list of URLs to check.
    """
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.content, 'xml')
    urls = [loc.text.strip() for loc in soup.find_all('loc')]  # Clean URLs
    print(f"Found {len(urls)} URLs in sitemap")
    return urls

def main(sitemap_url, output_option):
    """
    Main function that orchestrates the fetching of page sizes from a given sitemap.
    Outputs results either in the console or saves them to a CSV file.
    """
    urls = parse_sitemap(sitemap_url)
    page_sizes = []

    for url in tqdm(urls, desc="Processing pages"):
        total_size = find_assets(url)
        page_sizes.append((url, total_size))
    
    if output_option == 'console':
        # Print results to console
        print("URL | Pagesize (kB)")
        print("-" * 50)
        for url, size in page_sizes:
            print(f"{url} | {size:.2f} kB")
    elif output_option == 'file':
        # Save results to a CSV file in the outputs folder
        outputs_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'outputs'))
        os.makedirs(outputs_folder, exist_ok=True)  # Create outputs folder if it doesn't exist
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_csv = os.path.join(outputs_folder, f'page_sizes_{timestamp}.csv')
        df = pd.DataFrame(page_sizes, columns=['URL', 'Pagesize (kB)'])
        df.to_csv(output_csv, index=False)
        print(f"Results saved to {output_csv}")

# Prompt the user for output preference, repeating until a valid choice is made
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

# Provide the URL of your sitemap
sitemap_url = input("Enter the sitemap URL (must be a valid XML sitemap): ").strip()

# Call the main function with the provided arguments
main(sitemap_url, output_option)
