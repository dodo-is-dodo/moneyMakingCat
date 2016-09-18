from bs4 import BeautifulSoup
from urllib.request import urlopen

res = urlopen("http://www.naver.com").read().decode('utf-8')

soup = BeautifulSoup(res, 'lxml')

print(soup.prettify())
