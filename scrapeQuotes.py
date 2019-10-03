import requests, pprint
from time import sleep
from bs4 import BeautifulSoup
from random import choice
from csv import DictWriter

BASEURL = "http://quotes.toscrape.com"

def scrapeQuotes():
    allQuotes = []
    urlEnd = "/page/1/"
    while urlEnd:
        print(f"Now Scraping: {BASEURL}{urlEnd}.....")  #Just some text you can add at the top for something that may take a while.
        res = requests.get(f"{BASEURL}{urlEnd}")        #save response to res variable
        res.raise_for_status()                          #will halt program if download fails
        soup = BeautifulSoup(res.text, "html.parser")   #parser used to avoid an error

        quotes = soup.find_all(class_="quote") #class with underscore to not use keyword class
        for quote in quotes:
            allQuotes.append({
                "text":quote.find(class_="text").get_text(),
                "author":quote.find(class_="author").get_text(),
                "bio-link":quote.find("a")["href"] #finds anchor tag, and returns the href
            })

        nextButton = soup.find(class_="next")
        urlEnd = nextButton.find("a")["href"] if nextButton else None
        #sleep(1) #use this to pause between scrapes, so you don't get flagged
    return allQuotes

#write quotes to csv file
def writeQuotes(quotes):
    with open("quotes.csv", "w", encoding='utf-8') as file:
        headers = ["text", "author", "bio-link"]
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        for quote in quotes:
            csv_writer.writerow(quote)

quotes = scrapeQuotes()
writeQuotes(quotes)
