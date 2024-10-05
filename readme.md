# Bandwidth Buddy Tools

**Bandwidth Buddy Tools** is a set of Python scripts designed to help developers analyze and optimize web page performance by reducing bandwidth usage. These tools allow users to check the sizes of various assets on web pages, extract file sizes from sitemaps, and detect oversized resources that may affect website load time.

## Features

- **Page Size Checker**: Analyze the total size of assets (images, scripts, stylesheets, etc.) on web pages.
- **URL File Size Checker**: Check file sizes from a list of URLs to identify large resources.
- **Sitemap Size Checker**: Process sitemaps to extract URLs and check the sizes of the resources linked on those pages.
- **Customizable Thresholds**: Set size thresholds for reporting large files.

## Project Structure

```bash
bandwidth-buddy-tools/
├── src/
│   ├── sitemap_checker.py         # Script for checking file sizes from sitemaps
│   ├── url_checker.py             # Script for checking file sizes from a list of URLs
│   ├── page_size_checker.py       # Script for checking the page size of a webpage
├── outputs/                       # Directory where output CSV files will be saved
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/futurefounder/bandwidth-buddy-tools.git
cd bandwidth-buddy-tools
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

# Usage

### 1. Page Size Checker (from a list of URLs)

This tool analyzes the size of assets on a list of web pages. You can specify a list of URLs and a size threshold to report oversized assets.

Example usage:

```bash
python src/page_size_checker.py
```

You will be prompted to:

Enter a comma-separated list of URLs.
Choose between displaying results in the console or saving them to a file. 2. URL File Size Checker (from a list of URLs)
Checks the file size of resources (such as images, videos, or scripts) linked to a list of URLs.

Example usage:

bash
Copy code
python src/url_checker.py
You will be prompted to:

Enter a comma-separated list of URLs.
Specify a size threshold for reporting large assets. 3. Sitemap Size Checker
Extracts URLs from a sitemap and checks the size of the resources on those pages.

Example usage:

bash
Copy code
python src/sitemap_checker.py
You will be prompted to:

Enter the URL of a sitemap.
Choose between displaying results in the console or saving them to a file.
Example
Here’s an example of checking page sizes for a list of URLs:

Run the script:

bash
Copy code
python src/page_size_checker.py
Input URLs:

text
Copy code
Enter a comma-separated list of URLs (e.g., https://example.com/page1, https://example.com/page2):
Select Output:

text
Copy code
Do you want the results in the console or as a file? (press 'c' for console, 'f' for file, 'x' to exit):
View Results:

If you choose the file option, results will be saved in the outputs/ directory.

Contributing
Contributions are welcome! If you'd like to contribute to Bandwidth Buddy Tools, please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes and commit them (git commit -m 'Add some feature').
Push to the branch (git push origin feature-branch).
Open a Pull Request.
License
This project is licensed under the MIT License. See the LICENSE file for more details.

Author
Jesse Khala

For more information about the author, visit jessekhala.com.
