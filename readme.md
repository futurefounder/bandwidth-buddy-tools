# Bandwidth Buddy - Tools

**Bandwidth Buddy - Tools** is a set of Python scripts designed to help developers analyze and optimize web page assets and thereby reducing bandwidth usage. These tools allow users to check the sizes of various assets on web pages, extract file sizes from sitemaps, and detect oversized resources that may affect website bandwidth usage.

If used correctly, you can quickly dissect your website and optimize it for bandwidth efficiency and page speed.

## Features

- **Page Size Checker Sitemap**: Analyze the total size of assets (images, scripts, stylesheets, etc.) from a sitemap.
- **Page Size Checker URL**: Check file sizes from a list of URLs to identify large resources.
- **Sitemap Scanner**: Find any string in a given sitemap.
- **Customizable Thresholds**: Set size thresholds for reporting large files.

## Project Structure

```bash
bandwidth-buddy-tools/
├── src/
│   ├── pagesize_checker_sitemap.py       # Script for checking page sizes from a sitemap
│   ├── pagesize_checker_URLs.py          # Script for checking file sizes from a list of URLs
│   ├── sitemap_scanner.py                # Script for searching for an asset, or a string from a sitemap
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

### 🤏 1. Page Size Checker URLs

This tool analyzes the size of assets on a list of web pages. You can specify a list of URLs and a size threshold to report oversized assets.

Example usage:
Start the script with the command

```bash
python src/page_size_checker.py
```

You will be prompted to:

- Enter a comma-separated list of URLs.
- Specify a size threshold for reporting large assets.
- Choose between displaying results in the console or saving them to a file.

### 🗺️ 2. Page Size Checker Sitemap

This tool extracts URLs from a sitemap and checks the size of the resources on those pages.

You will be prompted to:

- Enter the URL of a sitemap.
- Choose between displaying results in the console or saving them to a file.

### 🔍 3. Sitemap Scanner

This tool scans an XML sitemap and checks the contents of each listed URL for specific search strings which you can use to find a specific asset, or other content on a site. The script allows you to output the results either in the console or save them to a CSV file for later analysis.

You will be prompted to:

- Enter the URL of a sitemap.
- Input search strings

# Contributing

Contributions are welcome! If you'd like to contribute to Bandwidth Buddy Tools, please follow these steps:

- Fork the repository.
- Create a new branch (git checkout -b feature-branch).
- Make your changes and commit them (git commit -m 'Add some feature').
- Push to the branch (git push origin feature-branch).
- Open a Pull Request.

# License

This project is licensed under the MIT License.
See the LICENSE file for more details.

# Author

Jesse Khala

For more information about the author, visit [jessekhala.com](htrtps://jessekhala.com).
