import requests
from twilio.rest import Client
from decouple import config

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
FUNCTION = "TIME_SERIES_DAILY"

MY_API = config("MY_API", default="")
NEW_API = config("NEW_API", default="")
TWILIO_SID = config("TWILIO_SID", default="")
TWILIO_TOKEN = config("TWILIO_TOKEN", default="")

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

parameters = {
    "function": FUNCTION,
    "symbol": STOCK_NAME,
    "apikey": MY_API
}

response = requests.get(url=STOCK_ENDPOINT, params=parameters)
response.raise_for_status()

data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_data = yesterday_data["4. close"]
print(yesterday_closing_data)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

difference = float(yesterday_closing_data) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "up"
else:
    up_down = "down"

diff_percent = (difference / float(yesterday_closing_data)) * 100
print(diff_percent)

if abs(diff_percent) > .1:
    news_params = {
        "apiKey": NEW_API,
        "qInTitle": COMPANY_NAME
    }

    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    print(articles)

    three_articles = articles[:3]
    print(three_articles)

    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. "
                          f"\nBrief {article['description']}" for article in three_articles]

    client = Client(TWILIO_SID, TWILIO_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="TWILIO PHONE NUMBER",
            to="RECEPIENT PHONE NUMBER",
        )
