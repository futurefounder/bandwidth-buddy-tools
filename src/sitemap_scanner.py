import requests
import xml.etree.ElementTree as ET
import urllib.parse
import csv
import datetime
import os

def check_string_in_source(url, search_strings):
    """
    Check if any of the search strings are present in the source code of the given URL.
    """
    encoded_url = urllib.parse.quote(url, safe=':/')
    response = requests.get(encoded_url)
    source_code = response.text
    return {search_string: search_string in source_code for search_string in search_strings}

def get_timestamped_filename(base_name, extension, folder):
    """
    Generate a timestamped filename for saving results to a file in the specified folder.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    return os.path.join(folder, f"{base_name}_{timestamp}{extension}")

def process_sitemap(sitemap_url, search_strings, output_option):
    """
    Process the sitemap and either print the results to the console or export to a CSV file.
    """
    try:
        response = requests.get(sitemap_url)
        sitemap_content = response.text

        # Parse the sitemap
        try:
            root = ET.fromstring(sitemap_content)
        except ET.ParseError:
            print("The provided URL does not point to a valid XML sitemap.")
            return

        urls = [element.text.strip() for element in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        total_urls = len(urls)

        results = []

        print("Index | URL | " + " | ".join([f"Contains '{search_string}'" for search_string in search_strings]) + " | Error")
        print("-" * 100)

        for index, url in enumerate(urls, start=1):
            try:
                found_strings = check_string_in_source(url, search_strings)
                result = [index, url] + ['🟢' if found else '🔴' for found in found_strings.values()] + ['']
                results.append(result)
                
                # Print result immediately
                print(" | ".join(map(str, result)))
                
                # Print progress to console
                print(f"Processed URL ({index}/{total_urls}): {url}")
            except requests.exceptions.RequestException as e:
                error_result = [index, url] + [''] * len(search_strings) + [str(e)]
                results.append(error_result)
                # Print error to console immediately
                print(" | ".join(map(str, error_result)))
                print(f"Error occurred for URL ({index}/{total_urls}): {url}")
                print(f"Error message: {str(e)}")

        # Handle output to file if selected
        if output_option == 'file':
            # Save results to a CSV file in the outputs folder
            outputs_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'outputs'))
            os.makedirs(outputs_folder, exist_ok=True)  # Create outputs folder if it doesn't exist
            output_file = get_timestamped_filename("results-sitemap", ".csv", outputs_folder)
            
            with open(output_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                header = ['Index', 'URL'] + [f"Contains '{search_string}'" for search_string in search_strings] + ['Error']
                writer.writerow(header)
                writer.writerows(results)
            print(f"Results saved to {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch the sitemap: {e}")

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

# Provide the URL of your sitemap and the search strings
sitemap_url = input("Enter the sitemap URL (must be a valid XML sitemap): ").strip()  # Generalized for user input
search_strings = input("Enter the search strings (comma-separated): ").split(',')

# Call the process_sitemap function with the provided arguments
process_sitemap(sitemap_url, [s.strip() for s in search_strings], output_option)
