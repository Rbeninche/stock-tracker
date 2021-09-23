import requests

STOCK_ENDPOINT = "https://www.alphavantage.co/query"

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_NAME = "MSFT"
STOCK_API_KEY = "BIBI2O23WJYHV4NO"
COMPANY_NAME = "microsoft"

NEWS_API_KEY = "e0372e23b59b4b23a4f9a8d55ab798dC"
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}
res = requests.get(STOCK_ENDPOINT, params=stock_params)
data = res.json()["Time Series (Daily)"]
data2 = res.json()["Meta Data"]["2. Symbol"]
print(data2)
print(type(data2))
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
print(difference)

diff_percent = (difference / float(yesterday_closing_price)) * 100
print(diff_percent)

if diff_percent > 0:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"][:5]

    article_description = [article['description'].replace("\r\n","") for article in articles]
    url = [article['url'] for article in articles]
    print(url)
    for index, article in enumerate(article_description):
        print(f"{index + 1} - {article}")
