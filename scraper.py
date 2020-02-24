import requests
from bs4 import BeautifulSoup
from statistics import mean
from decimal import Decimal
TWOPLACES = Decimal(10) ** -2

def scrape(trademe):
    finished = False
    pageNum = 1
    fullList = []
    try:
        while not finished:
            response = requests.get("%s?buy=buynow&page=%d" %(trademe,pageNum))
            pageNum += 1
            soup = BeautifulSoup(response.text, "html.parser")
            totalCount = int(soup.find("span", {"id":"totalCount"}).text.strip())
            lowCount = int(soup.find("span", {"id":"lowCount"}).text.strip())
            if lowCount < totalCount and pageNum < totalCount:
                itemlist = soup.findAll("a")
                fullList += itemlist
            else:
                finished = True
        return fullList
    except:
        return None

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
                break # do nothing
        else:
            processedList.append({"title":item_title, "price":item_price, "url":item_url})
    return processedList

def stripMoney(val):
    price = Decimal(val.lstrip("$")).quantize(TWOPLACES)
    return price

def priceProcess(theList):
    mini = stripMoney(theList[0]["price"])
    maxi = stripMoney(theList[0]["price"])
    ave = 0
    prices = []
    for item in theList:
        price = stripMoney(item["price"])
        if price < mini:
            mini = price
        if price > maxi:
            maxi = price
        prices.append(price)
    ave = mean(prices).quantize(TWOPLACES)
    return mini, maxi, ave


# For testing
# trademe = "https://www.trademe.co.nz/computers/tablets-ebook-readers/ebook-readers"
# theList = process(scrape(trademe))
# print(theList)
# mini, maxi, ave = priceProcess(theList)
# print(mini, maxi, ave)