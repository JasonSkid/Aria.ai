import yfinance as yf
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os  # Make sure this line is present

def get_fortune_500_symbols():
    # Fetch the current list of Fortune 500 companies from a source
    # For example, you can use the Wikipedia page for the Fortune 500 list
    # https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue

    # Replace the URL with the actual URL of the Fortune 500 list
    url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'
    
    # Send a request to the URL and get the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all tables on the page
    tables = soup.find_all('table')

    for i, table in enumerate(tables):
        # Assuming the stock symbols are in the first column of the table
        symbols = [row.find_all('td')[0].text.strip() for row in table.find_all('tr')[1:]]
        
        if symbols:
            print(f"Symbols found in table {i + 1}")
            return symbols

    print("No tables found on the page or symbols in any table.")
    return []

def record_stock_data(api_key, companies, output_dir):
    for symbol in companies:
        stock_data = fetch_stock_data(api_key, symbol)
        if not stock_data.empty:
            filename = os.path.join(output_dir, f'{symbol}_stock_data.csv')
            stock_data.to_csv(filename)
            print(f'Stock data for {symbol} recorded in {filename}')

def fetch_stock_data(api_key, symbol, interval='1d', output_size='compact'):
    ts = yf.Ticker(symbol)
    historical_data = ts.history(period='3mo', interval=interval)
    
    return historical_data

def get_nyse_symbols(api_key):
    endpoint = 'https://www.alphavantage.co/query'
    function = 'LISTING_STATUS'
    params = {
        'apikey': api_key,
        'exchange': 'NYSE',
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    if 'status' in data and data['status'] == 'active':
        status_column = 'status'  # Adjust this based on the actual column name in the response
        symbol_column = 'symbol'  # Adjust this based on the actual column name in the response
        active_symbols = data.get('data', {}).get('rows', [])
        return [symbol['symbol'] for symbol in active_symbols]
    else:
        print("Invalid response format. Check the Alpha Vantage API response format.")
        return []

if __name__ == "__main__":
    alpha_vantage_api_key = 'Y439VIMJJTNWCSXE'  # Replace with your Alpha Vantage API key

    fortune_500_symbols = get_fortune_500_symbols()
    output_directory = 'stock_data'
    os.makedirs(output_directory, exist_ok=True)

    record_stock_data(alpha_vantage_api_key, fortune_500_symbols, output_directory)

    nyse_symbols = get_nyse_symbols(alpha_vantage_api_key)
    record_stock_data(alpha_vantage_api_key, nyse_symbols, output_directory)
