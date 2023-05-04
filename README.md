# Tagger - An extremely simple CLI frontend to BeautifulSoup
# If you're interested in using this for some reason, you're probably better off using [htmlq](https://github.com/mgdm/htmlq).
# Author: Dellon Zerus
# All code licensed under GPLv3

Tagger is a small command line utility written in Python, using bs4 to scrape web pages. I wrote it as a practice tool way back when, but it's not very useful.

Note: Originally intended, and tested only for Linux.

## Features:
- Usable from command line
- Write output to html file
- Save pages to file

## Usage examples:
### Output contents of every paragraph:
`tagger example.com --tag p --attribute inner`

### Output every link:
`tagger -t a -a href example.com`

### Search for all tags in a class named test
`tagger -s class test example.com`

## Dependencies:
- python3 - The language
- pip3 - The installer (optional if you install the modules manually)
- bs4 - For the actual scraping
- requests module - For getting the webpage
- argparse module - For handling the command-line arguments
- gzip - For handling man page

## Installation instructions:
```
sudo -i
git clone https://github.com/DZerus/tagger
cd tagger
chmod +x install.sh && ./install.sh
tagger
```
