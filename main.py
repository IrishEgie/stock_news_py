import requests as rq
from config import *
import smtplib 

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_params = {
    "function":"TIME_SERIES_INTRADAY",
    "symbol":"IBM",
    "interval":"1min",
    "apikey":stock_api_key
}
stock_response = rq.get("https://www.alphavantage.co/query?", params=stock_params)
stock_data = stock_response.json() #Type Dictionary

# Extract the time series data (Type: Dictionary)
time_series = stock_data["Time Series (Daily)"]

# Get the first two dates (most recent two)
dates = list(time_series.keys())
most_recent = dates[0]
previous = dates[1]

# Extract the "close" values for both dates
most_recent_close = float(time_series[most_recent]["4. close"])
previous_close = float(time_series[previous]["4. close"])

# Calculate the difference
price_difference = most_recent_close - previous_close

# Check if the difference is equal to or greater than 5
if abs(price_difference) >= 5:
    print(f"Stock price changed by {price_difference:.2f}, which is 5 or more.")
else:
    print(f"Stock price changed by {price_difference:.2f}, which is less than 5.")

# print(news_data)

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

# news_params = {
#     "country": "us",
#     "category":"business",
#     "apiKey":news_api_key

# } 

# news_response = rq.get("https://newsapi.org/v2/top-headlines?", params=news_params)
# news_data = news_response.json()["articles"] # Type List

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

def send_email():
    with smtplib.SMTP("smtp.gmail.com",587) as connection:
        connection.starttls()
        connection.login(user=EMAIL,password=EMAIL_APP_PASS)
        connection.sendmail(from_addr=EMAIL,to_addrs=send_to,msg=f"Subject: Headline:{news_data[0]["title"]} \n\n Brief:{news_data[0]["description"]}")

#Optional: Format the SMS message like this: 


"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

