import requests
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from speech_output import speak

API_KEY = 'GQOKWXUEENYN4M2G'

def get_stock_price(symbol):
    """
    Fetches the current price of the given stock symbol using Alpha Vantage API.
    """
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'Global Quote' in data and '05. price' in data['Global Quote']:
            price = data['Global Quote']['05. price']
            #round price to hundreths place
            price = round(float(price), 2)
            dollars = int(price)
            cents = int((price - dollars) * 100)
            speak(f"The current price of {symbol} is {dollars} dollars and {cents} cents.")
        else:
            
            speak(f"Could not find price information for {symbol}.")
    else:
        speak("Failed to fetch stock data due to an error with the API.")

def stock_commands(command):
    """
    Processes a command related to stock prices.
    """
    print(command.lower())
    command = command.lower()
    if "get price of " in command:
        symbol = command.split("get price of ")[1].strip("'").upper()
        get_stock_price(symbol)
    else:
        speak("Stock command not recognized.")

