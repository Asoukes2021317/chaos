import scraper

def test_scrape1():
    output = scraper.scrape("nothing")
    assert output == None
def test_scrape2():
    output = scraper.scrape("http://massey.ddns.net/~youngt68400/blah.html")
    assert len(output) > 0

def test_process1():
    output = scraper.scrape("http://massey.ddns.net/~youngt68400/blah.html")
    assert scraper.process(output) == [{'title': 'Example Title', 'price': '$2', 'url': 'https://www.trademe.co.nz/computers'}, {'title': 'Example Title2', 'price': '$3', 'url': 'https://www.trademe.co.nz/computers'}]

def test_stripMoney():
    assert scraper.stripMoney("$3") == 3

def test_priceProcess():
    mini, maxi, ave = scraper.priceProcess([{'title': 'Example Title', 'price': '$1.50', 'url': 'https://www.trademe.co.nz/computers'}, {'title': 'Example Title2', 'price': '$3', 'url': 'https://www.trademe.co.nz/computers'}])
    assert mini == 1.5
    assert maxi == 3
    assert ave == 2.25