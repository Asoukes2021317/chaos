import requests
from bs4 import BeautifulSoup
from statistics import mean
from decimal import Decimal
TWOPLACES = Decimal(10) ** -2

trademe = "https://www.trademe.co.nz/computers/tablets-ebook-readers/ebook-readers"

def scrape(trademe):
    finished = False
    pageNum = 1
    fullList = []
    while not finished:
        response = requests.get("%s?buy=buynow&page=%d" %(trademe,pageNum))
        pageNum += 1
        soup = BeautifulSoup(response.text, "html.parser")
        totalCount = int(soup.find("span", {"id":"totalCount"}).text.strip())
        lowCount = int(soup.find("span", {"id":"lowCount"}).text.strip())
        if lowCount < totalCount:
            itemlist = soup.findAll("a")
            fullList += itemlist
        else:
            finished = True
    return fullList

def process(theList):
    processedList = []
    for theItem in theList:
        try:
            item_title = theItem.find("div", {"class":"title"}).text.strip()
            item_price = theItem.find("div", {"class":"listingBuyNowPrice"}).text.strip()
        except AttributeError:
            continue # go to next item, adverts won't be added

        item_url = "https://www.trademe.co.nz"+theItem['href']

        for item in processedList:
            if item["title"] == item_title and item["price"] == item_price:
                # do nothing
                break
        else:
            processedList.append({"title":item_title, "price":item_price, "url":item_url})
    
    return processedList

def priceProcess(theList):
    mini = theList[0]["price"]
    maxi = theList[0]["price"]
    ave = 0
    prices = []
    for item in theList:
        price = Decimal(item["price"].lstrip("$")).quantize(TWOPLACES)
        if price < mini:
            mini = price
        if price > maxi:
            maxi = price
        prices.append(price)
    ave = mean(prices).quantize(TWOPLACES)
    print(mini+maxi+ave)
    