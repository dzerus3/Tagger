#!/usr/bin/python3
# Made by: Dellon Zerus

__version__ = "3.0 Usable"

from sys import exit

#Logo; Font by patorjk, found on his website at http://patorjk.com
banner = """ 
\033[92m
 /$$$$$$$$                                               
|__  $$__/                                               
   | $$  /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$ 
   | $$ |____  $$ /$$__  $$ /$$__  $$ /$$__  $$ /$$__  $$
   | $$  /$$$$$$$| $$  \ $$| $$  \ $$| $$$$$$$$| $$  \__/
   | $$ /$$__  $$| $$  | $$| $$  | $$| $$_____/| $$      
   | $$|  $$$$$$$|  $$$$$$$|  $$$$$$$|  $$$$$$$| $$      
   |__/ \_______/ \____  $$ \____  $$ \_______/|__/      
                  /$$  \ $$ /$$  \ $$                    
                 |  $$$$$$/|  $$$$$$/                    
                  \______/  \______/                     
\033[0m
\033[92mTagger\033[0m - A simple command line interface for BeautifulSoup

Made by Dellon Zerus
Version: {0}
"""

def main():
    scrape()
    return 

#Checks whether user passed arguments.
def checkArgs():
    from sys import argv

    if len(argv) <= 2:
        print(banner.format(__version__))
        print("Looks like you didn't pass enough arguments.")
        print("Try \033[1m{0} --help\033[0m for a manual.".format(argv[0]))
        exit(0)
    return

def scrape():
    from bs4 import BeautifulSoup

    #Reads args from stdin
    args, link = parseArgs()

    #If user specified the --version argument, we do not need to do anything else
    if args.version:
        print(__version__)
        exit(0)
   
    #If at this point the program did not exit and there was only one argument (valid ones would be -h/--help, or -v/--version) then we exit.
    checkArgs()
 
    #Retrieve HTML from either file or link (if both are specified it will only get the file)
    html = getHTML(args.fname, link)

    #html contents bs works with
    soup = BeautifulSoup(html, "html.parser")

    sortElements(soup, args)

def sortElements(soup, args):
    #A buffer for all the elements we are working with
    saved = ""

    #A buffer to hold attribute contents if we are looking for those.
    #Unused if we are not looking for those
    attrs = []

    #There can only be one element with certain id so finish program right after
    if args.id:
        getArgsById(saved, soup, args);
        return

    #We handle tagname specially when searching for class
    if args.tagname and not args.sattr:
        saved = soup.findAll(args.tagname)
        #If the given tag was not found, there is no point in searching further
        if not saved:
            print("Given tag was not found")
            return
    
    #Probably used for searching for classes
    if args.sattr:
        #This is because we shouldn't set args.tagname directly, but empty string counts as "search by all tags"
        tags = args.tagname
        if not tags:
            tags = ""
        saved = soup.findAll(tags, {args.sattr[0]:args.sattr[1]}) 
        
    if args.attr:
        attrs = retrieveAttribute(saved, args.attr[0])
    finish(attrs, args.ofile, saved, soup.prettify)

#Prints out results on screen or writes it to specified output file.
def finish(attrs, ofilename, saved, prettified):
    if attrs:
        for item in attrs:
            print(item)
    elif ofilename:
        with open(ofilename, "w") as outfile:
            outfile.write(str(prettified))
    else:
        for item in saved:
            print(item)

def getArgsById(saved, soup, args):
        saved = soup.findAll(id=args.id)
        if not saved:
             print("Element with given ID was not found")
        finish("", args.ofile, saved, soup.prettify)

def retrieveAttribute(saved, givenattr):
    #A buffer for attributes read from the elements in saved
    attrs = []
	
    #Just prints whatever is in between the tag then
    if givenattr == "inner":
        for element in saved:
            attrs.append(element.text) 
    else:
        for element in saved:
            try:
                attributevalue = element[givenattr]
                attrs.append(attributevalue)
            except KeyError:
                pass
    if not attrs:
        print("Given attribute was not found. Exiting.")
        exit(0)
    return attrs

def getHTML(fname, link): 
    #If user specified a file to read...
    if fname:
        html = getFile(fname)
    
    #If user specified a link to get...
    elif link:
        html = getLink(link[0])

    #If there is no link and no file name    
    else:
        print("Could not find link or filename. Are you sure you specified one?")
        exit(0)
    return html 

#Retrieves HTML from link if user passed link
def getLink(link):
    import requests
    
    verifyURL(link)

    #Check if the link has a schema and add one if it does not 
    if "http://" not in link and "https://" not in link:
        print("Your link did not contain a schema. Adding one right now...")
        link = "http://" + link

    #Testing has shown that this may not be favorable. I will leave here for now.
    if "www." in link:
        print("Prepending \"www.\" to your link might have unexpected effects")
    
    #Check for invalid URL, or generic errors
    try:
        source = requests.get(link)
        print("Retrieved website at {0}.\n HTTP Status Code: {1}".format(link, source.status_code))

    except Exception as e:
        print("An error occured while getting page: ", e)
        exit(1)
    
    return source.content

def verifyURL(url):
    from socket import gethostbyname
    #Note: some DNS servers redirect all invalid URLs to a "wrong URL" server
    #As such, even wrong URLs can sometimes pass as normal
    try:
        gethostbyname(url)
    except:
        print("Failed to resolve host {0}. Are you sure you typed the name in correctly?".format(url))
        exit(1)

#Retrieves HTML from file if user passed file name
def getFile(fname):
    try:
        html = ""
        with open(fname, "r") as file:
            for line in file.readlines():
                html += line
        return html
    
    #Error handling
    except FileNotFoundError:
        print("You supplied an invalid file path. Are you sure {0} exists?".format(fname))
        exit(1)
    
    except Exception as e:
        print("An error occured while reading from file: ", e)
        exit(1)

#Handles whatever user passed as argument. 
def parseArgs():
    import argparse

    parser = argparse.ArgumentParser(
            description="Tagger - A simple command line web scraper", 
            epilog="For more in-depth instruction check out the man page") 
    
    help_texts={
            "vrsn"   : "Output program version and exit.",
            "tag"    : "Indicate which tag you want to look for.",
            "id"     : "Search for element with given id value.",
            "sattr"  : "Search for items with an attribute that matches given value (especially usable when searching by class)",

            "attr"   : "Only output the value of given attribute.",
            "file"   : "Specify html file to read. (note: advisable for repeated queries)",
            "output" : "Take edited html and output it to an html file.",
    }

    parser.add_argument("-v", "--version",     action="store_true", dest="version", help=help_texts["vrsn"])
    parser.add_argument("-t", "--tag",         nargs = "+", action="store", dest="tagname", 	help=help_texts["tag"])
    parser.add_argument("-i", "--id",          nargs = "+", action="store", dest="id", 	        help=help_texts["id"])
    parser.add_argument("-a", "--attr",        nargs = "+", action="store", dest="attr", 	    help=help_texts["attr"])
    parser.add_argument("-s", "--search-attr", nargs = "+", action="store", dest="sattr",       help=help_texts["sattr"])
    parser.add_argument("-f", "--file",        action="store", dest="fname", 	help=help_texts["file"])
    parser.add_argument("-o", "--output",      action="store", dest="ofile",  	help=help_texts["output"])

    return parser.parse_known_args() 

main()