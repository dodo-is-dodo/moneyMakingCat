# -*- coding: UTF-8 -*-
import csv
import urllib.request
from bs4 import BeautifulSoup
import re
mov_list = open("Cannes.txt", "rt")
p = re.compile("(\d{1,3},){0,}\d{1,3}")
f  = open('Cannes.csv', "wt")
writer = csv.writer(f, delimiter=',', quotechar='"')

lines = mov_list.readlines()
prize = "Cannes"
home = "http://www.imdb.com/"
for i in lines:
	bs = False
	gs = False
	if i == "":
		break
	html = urllib.request.urlopen(i[:len(i)-2])
	soup = BeautifulSoup(html, "html.parser")
	f.write(prize + ", ")
	title = soup.findAll('span', attrs={'class':'itemprop'})
	try:
		f.write(title[0].text + ", ")
	except UnicodeEncodeError:
		f.write("NONE" +", ")
	director = soup.findAll('div', attrs={'itemprop':'director'})
	try:
		f.write(director[0].a.span.text + ", ")
	except UnicodeEncodeError:
		f.write("NONE" +", ")
	rating = soup.findAll('div', attrs={'class':'star-box-giga-star'})
	if rating:
		f.write(rating[0].text + ", ")
	else:
		f.write("NONE" +", ")
	time = soup.findAll('time', attrs={'itemprop':'duration'})
	if time:
		f.write(p.findall(time[0].text)[0] + ", ")
	else:
		f.write("NONE, ")
	gb = soup.findAll('div', attrs={'class':'txt-block'})
	for i in gb:
		if i.h4:
			if i.h4.text == "Budget:":
				budget = i.text
				bs = True
			elif i.h4.text == "Gross:":
				gross = i.text
				gs = True

	if gs == True:
		gro = p.search(gross)
		f.write(gro.group(0).replace(",", "") + ", ")
	else:
		f.write("NONE, ")

	if bs == True:
		bud = p.search(budget)

		f.write(bud.group(0).replace(",", ""))
	else:
		f.write("NONE")

	genre = soup.findAll('span', attrs={'itemprop':'genre'})
	for i in genre:
		f.write(", " + i.text)
	f.write("\n")
f.close()
mov_list.close()
