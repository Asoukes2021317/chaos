import requests
from bs4 import BeautifulSoup
from scraper import scrape
from statistics import mean
from decimal import Decimal
import csv
import time
import pathlib

TWOPLACES = Decimal(10) ** -2
trademe = "https://www.trademe.co.nz/gaming/playstation-4/consoles"
#trademe = "https://www.trademe.co.nz/computers/tablets-ebook-readers/ebook-readers"
itemlist = scrape(trademe)
ps4List = []

for i, item in enumerate(itemlist):
    try:
        item_title = item.find("div", {"class":"title"}).text.strip()
        item_price = item.find("div", {"class":"listingBuyNowPrice"}).text.strip()
    except AttributeError:
        continue # go to next item, adverts won't be added

    item_url = "https://www.trademe.co.nz"+item['href']

    for ps4 in ps4List: # it took me so long to figure this out nicely, I'm assuming it mean TITLE AND PRICE not TITLE AND TITLE
        if ps4[0] == item_title and ps4[1] == item_price:
            # do nothing
            break
    else:
        #if "ps4" in item_title.lower() or "playstation 4" in item_title.lower():
        ps4List.append([item_title, item_price, item_url])

# SHOW INFO
mini = 1000000000 # probs not best way to do it, but if there's nothing smaller than 1 billion something is probably wrong
maxi = 0
ave = 0
prices = []
for ps4 in ps4List:
    print(ps4[0], "-", ps4[1])
    price = Decimal(ps4[1].lstrip("$")).quantize(TWOPLACES)
    if price < mini:
        mini = price
    if price > maxi:
        maxi = price
    prices.append(price)
print("There are %d PS4 consoles on TradeMe." %(len(ps4List)))
print("The minimum cost of a PS4 console is $%d" %(mini))
print("The maximum cost of a PS4 console is $%d" %(maxi))
ave = mean(prices).quantize(TWOPLACES)
print("The average cost of a PS4 console is $%d" %(ave))

# CSV Stuffs
header = ["Title", "Price", "URL"]
fname = time.strftime("%Y-%m-%d_%H-%M-%S_scrape.csv")
location = pathlib.Path(__file__).parent / fname
with open(location, 'wt', newline='\n') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(header)
    for ps4 in ps4List:
        csv_writer.writerow(ps4)