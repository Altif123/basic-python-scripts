import pprint

import requests
from bs4 import BeautifulSoup


def find_bio(username):
    c = format("https://twitter.com"+"/" + username)
    r = requests.get(c)
    s = BeautifulSoup(r.text, "html.parser")

    return s.find("div", class_="ProfileHeaderCard").text


def find_toptweet(username):
    c = format("https://twitter.com"+"/" + username)
    r = requests.get(c)
    s = BeautifulSoup(r.text, "html.parser")

    return s.find("div", class_="content").text


if __name__ == "__main__":
    username = input('enter username: ')
    bio = find_bio(username).replace("\n", " ")
    tweet = find_toptweet(username).replace("\n", " ")
    print("Bio--------------------------------------------------------------------------------------")
    pprint.pprint(bio)
    print("End of Bio--------------------------------------------------------------------------------------\n\n\n\n")
    print('top tweet')
    pprint.pprint(tweet)

