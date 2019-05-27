import requests
from bs4 import BeautifulSoup

search = "https://www.google.com/search?q={}"
term = "meaning of {} in {}"


def meaning(word, language):
    query = search.format(term.format(word, language))
    r = requests.get(query)
    s = BeautifulSoup(r.text, "html.parser")
    return s.find("div", class_="AP7Wnd").text


if __name__ == "__main__":
    word = input("Enter the word you want to find the translation of: ")
    lang = input("Language you want the meaning translated to: ")
    newword = meaning(word, lang)
    print(newword)
