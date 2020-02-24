from flask import Flask, render_template
import scraper

app = Flask(__name__)

trademe = "https://www.trademe.co.nz/computers/tablets-ebook-readers/ebook-readers"
theList = scraper.process(scraper.scrape(trademe))
scraper.priceProcess(theList)
@app.route("/")
def home():
    return render_template("index.html", len=len(theList), items=theList)
    
if __name__ == "__main__":
    app.run(debug=True)