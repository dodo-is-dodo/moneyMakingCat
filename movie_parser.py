import urllib.request
from bs4 import BeautifulSoup


f  = open('test.csv', "wt")
writer = csv.writer(f, delimiter=' ', quotechar='|')


home = "http://www.imdb.com/"
html = urllib.request.urlopen('http://www.imdb.com/name/nm0000759/?ref_=fn_al_nm_1')
soup = BeautifulSoup(html, "html.parser")
movies = soup.findAll('div', attrs={'class':'filmo-row'})
count = 20
for i in movies:
	if not count:
		break
	page = home + i.b.a["href"]
	H = urllib.request.urlopen(page)
	S = BeautifulSoup(H, "html.parser")
	title = S.findAll('span', attrs={'class':'itemprop'})
	rating = S.findAll('div', 'titlePageSprite star-box-giga-star')
	print(title[0].text)
	try:
		print(rating[0].text)
	except IndexError:
		writer.writerow([title[0].text, "blank"])
	else:
		writer.writerow([title[0].text, rating[0].text])
	count -=1
f.close()
