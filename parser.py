#Creator VLAN#9796
from bs4 import BeautifulSoup
import requests
from collections import Counter
import os
from random import randrange

minpice = 999999999999
maxprice = 0
totalprice = 0
countprice = 0
errors = 0
file = None

produkt = str(input("Введите тавар для парсинга - "))
count = int(input("Сколько страниц парсить - "))
slova = int(input("Сколько ключевых слов вам показать - "))

def eche(Counter):
	yesorno = str(input("Продолжаем ? (да или нет) - "))
	if yesorno == "Да" or yesorno == "да":
		produkt = str(input("Введите тавар для парсинга - "))
		count = int(input("Сколько страниц парсить - "))
		slova = int(input("Сколько ключевых слов вам показать - "))
		start(produkt, count ,slova , Counter)
	elif yesorno == "Нет" or yesorno == "нет":
		pass
	else:
		print("Напишите точно 'да' или 'нет'")
		eche(Counter)

def end(produkt, count ,slova ,names, minpice, maxprice, totalprice ,countprice ,errors , Counter , namef):
	from collections import Counter
	split_it = names.split()
	Counter = Counter(split_it)
	most_occur = Counter.most_common(slova)
	print("Статистика")
	print("---------слово - сколько раз использовалось---------")
	print(most_occur)
	print("--------средная цена----------")
	sredprice = int(totalprice)/int(countprice)
	print("общая цена - "+str(totalprice)+" . запросов обработано - "+str(countprice))
	print(sredprice)
	print("--------цены от и до----------")
	print(str(minpice)+" - "+str(maxprice))
	print("--------ошибок----------")
	print(errors)
	print("------------------")
	print(f"Все товары записанны в файле {namef} \nОн находитья в той же папке что и этот код")
	eche(Counter)


def start(produkt, count ,slova , Counter):
	THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
	namef = f"history{randrange(1000000000000)}.txt"
	my_file = os.path.join(THIS_FOLDER, namef)
	file = open(namef , "a+" , encoding="utf-8")
	url = "https://www.avito.ru/rossiya?q="+produkt
	if count > 1:
		url = url+ "&p=" + str(count)
	request = requests.get(url)
	soup = BeautifulSoup(request.text , "html.parser")
	names = ""
	minpice = 999999999999
	maxprice = 0
	totalprice = 0
	countprice = 0
	errors = 0
	while count - 1 >= 1 :
		produkts = soup.find_all("div",class_="iva-item-body-R_Q9c")
		print("Выполняем")
		for prod in produkts:
			price = prod.find('div',{"class":"iva-item-priceStep-QN8Kl"}).find('span',{"class":"price-price-BQkOZ"}).find('meta',{"itemprop":"price"})["content"]
			papka = prod.find('div',{"class":"iva-item-titleStep-_CxvN"}).find('a',{"class":"link-link-MbQDP link-design-default-_nSbv title-root-j7cja iva-item-title-_qCwt title-listRedesign-XHq38 title-root_maxHeight-SXHes"})
			if papka is None:
				print("ошибка1")
				errors += 1
			else:
				if price == "...":
					price = "Цена не указанна"
				name = papka["title"]
				urlp = papka["href"]
				file.write(f"{name} - {price}\nhttps://www.avito.ru{urlp}\n")
				#статистика
				if price == "Цена не указанна":
					pass
				elif int(price) > int(maxprice):
					maxprice = price
					totalprice = totalprice + int(price)
					countprice += 1
				elif int(price) < int(minpice):
					minpice = price
					totalprice = totalprice + int(price)
					countprice += 1
				else:
					totalprice = totalprice + int(price)
					countprice += 1
				names = names+" "+ name
				file.write("------------------\n")
		count = count - 1
		print("!!!!!Страница - "+str(count))
	end(produkt, count ,slova ,names, minpice, maxprice, totalprice ,countprice ,errors , Counter , namef)
start(produkt, count ,slova , Counter)
