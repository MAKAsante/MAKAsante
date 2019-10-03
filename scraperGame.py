#http://quotes.toscrape.com
#todo don't forget about this funciton!

import requests, pprint
from time import sleep
from bs4 import BeautifulSoup
from random import choice
from csv import DictReader

def readQuotes(filename):
    with open(filename, "r", encoding='utf-8') as file:
        csv_reader = DictReader(file)
        return list(csv_reader)

BASEURL = "http://quotes.toscrape.com"

def startGame(quotes):
    quote = choice(quotes)
    remainingGuesses = 4
    print(f"Here's a quote: \n{quote['text']}")
    print(quote["author"])

    guess = ""
    while guess.lower() != quote["author"].lower() and remainingGuesses > 0:
        guess = input(f"Who said this quote? Guessed remaining: {remainingGuesses}\n")
        remainingGuesses -= 1
        if guess.lower() == quote['author'].lower():
            print(f"Congratulations! You got the correct answer!")
            break
        if remainingGuesses == 3:
            res = requests.get(f"{BASEURL}{quote['bio-link']}")
            soup = BeautifulSoup(res.text, "html.parser")
            birthDate = soup.find(class_="author-born-date").get_text()
            birthPlace = soup.find(class_="author-born-location").get_text()
            print(f"Here's a hint:\nThe author was born in {birthPlace} on {birthDate}")
        elif remainingGuesses == 2:
            print(f"Here's another hint:\nThe author's first name begins with {quote['author'][0]}")
        elif remainingGuesses == 1:
            lastInitial = quote["author"].split(" ")[1][
                0]  # 1 gives first item in list of names (last name). 0 gives first character of that
            print(f"The author's last name begins with {lastInitial}")
        else:
            print(f"Sorry, you ran out of guesses. The answer was {quote['author']}")

    again = ""
    while again not in ("y", "yes", "n", "no"):
        again = input(f"Would you like to play again? (y/n)\n")
        if again.lower() in ("y" "yes"):
            print(f"Restarting the game! Goodluck!")
            return startGame(quotes)
        else:
            print(f"Alrighty! Goodbye!")

quotes = readQuotes("quotes.csv")
startGame(quotes)
