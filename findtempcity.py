import requests
from bs4 import BeautifulSoup

q = "https://www.google.com/search?q={}"


def find_temperature(city):
    c = q.format("weather in" + city)
    r = requests.get(c)
    s = BeautifulSoup(r.text, "html.parser")
    return s.find("div", class_="BNeawe iBp4i AP7Wnd").text
    #return s.findAll("span")


if __name__ == "__main__":
    temp = find_temperature("leeds")
    print(temp)
