import requests
from bs4 import BeautifulSoup

response = requests.get('http://www.showmeboone.com/sheriff/JailResidents/JailResidents.asp')
html = response.content

soup = BeautifulSoup(html, "html.parser")

print(soup.prettify())
