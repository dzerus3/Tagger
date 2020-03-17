### Tagger - An extremely simple CLI frontend to BeautifulSoup
### Author: Dellon Zerus
### All code licensed under GPLv3

Tagger is a small command line utility written in Python, using bs4 to scrape web pages. 

Note: Originally intended, and tested only for Linux.

## Features:
- Usable from command line
- Write output to html file
- Save pages to file

## Usage examples:
# Output contents of every paragraph:
`tagger example.com --tag p --attribute inner`

# Output every link:
`tagger -t a -a href example.com`

# Search for all tags in a class named test
`tagger -s class test example.com`

## Dependencies:
- python3 - The language
- pip3 - The installer (not necessary if you can install the modules manually)
- bs4 - For the actual scraping
- requests - For getting the webpage
- argparse - For handling the command-line arguments
- gzip - For handling man page

## Installation instructions:
```
sudo -i
git clone https://github.com/DZerus/tagger
cd tagger
chmod +x install.sh && ./install.sh
tagger
```
