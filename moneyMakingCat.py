from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

req = Request("https://www.grailed.com", headers={'User-Agent': 'Mozilla/5.0'})
res = urlopen(req).read().decode('utf-8')

soup = BeautifulSoup(res, 'lxml')

print(soup.prettify())
# items = soup.find_all('div', attrs={'class':"feed-item"})

# for item in items:
#     print(item)
