import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = 'you`r api key'
STOCK_ENDPOINT = 'https://www.alphavantage.co/query'
NEWS_API_KEY = 'ff61ed54bcf9495fa1d7383d178f0830'
NEWS_ENDPOINT = 'https://newsapi.org/v2/everything'
TWILIO_SID = 'you`r sid'
TWILIO_TOKEN = 'you`r token'

VIRTUAL_TWILIO_NUMBER = "you`r number"
VERIFIED_NUMBER = "you`r number"



stock_params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data['4. close']
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data['4. close']
print(day_before_yesterday_closing_price)

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
print(difference)

up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

dif_percent = (difference / float(yesterday_closing_price)) * 100
print(dif_percent)



# Instead of printing ("Get News"), geting the first 3 news pieces for the COMPANY_NAME.

if abs(dif_percent) > 0:
    news_params = {
        'apiKey': NEWS_API_KEY,
        'qInTitle': COMPANY_NAME
    }
    new_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = new_response.json()['articles']
    three_articles = articles[:3]
    print(three_articles)



# Send a seperate message with the percentage change and each article's title and description to your phone number.

formatted_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
print(formatted_articles)

client = Client(TWILIO_SID, TWILIO_TOKEN)
for article in formatted_articles:
    message = client.messages.create(
        body=article,
        from_=VIRTUAL_TWILIO_NUMBER,
        to=VERIFIED_NUMBER
    )
    print(message.sid)
