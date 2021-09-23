from flask import Flask, render_template, request, redirect, url_for
import requests
from stocks import STOCK_API_KEY, STOCK_ENDPOINT, NEWS_ENDPOINT, NEWS_API_KEY

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/info')
def info():
    stock_name = request.args.get('stock_name').upper()
    company_name = request.args.get('company_name')
    stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": stock_name,
        "apikey": STOCK_API_KEY
    }
    res = requests.get(STOCK_ENDPOINT, params=stock_params)
    check_stock_name = res.json()["Meta Data"]["2. Symbol"]
    data = res.json()["Time Series (Daily)"]

    data_list = [value for (key, value) in data.items()]
    yesterday_data = data_list[0]
    yesterday_closing_price = yesterday_data["4. close"]
    print(yesterday_closing_price)

    day_before_yesterday_data = data_list[1]
    day_before_yest_closing_price = day_before_yesterday_data["4. close"]
    print(day_before_yest_closing_price)

    difference = abs(float(yesterday_closing_price) - float(day_before_yest_closing_price))
    print(difference)

    diff_percent = (difference / float(yesterday_closing_price)) * 100
    article_description = None
    if diff_percent > 0:
        news_params = {
            "apiKey": NEWS_API_KEY,
            "qInTitle": company_name
        }

        news_response = requests.get(NEWS_ENDPOINT, params=news_params)
        articles = news_response.json()["articles"][:5]

        article_description = [article['description'].replace("\r\n", "") for article in articles]
        url = [article['url'] for article in articles]

    return render_template('info.html', yesterday=yesterday_closing_price, day_before=day_before_yest_closing_price,
                           articles=article_description, difference=diff_percent, stock_name=stock_name, company_name=company_name)


@app.route('/error')
def error():
    return '<h1>Bad input. Please enter a stock sticker again <a href ="/" Go back</a></h1>'


if __name__ == '__main__':
    app.run(debug=True)
