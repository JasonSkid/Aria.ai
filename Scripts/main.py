import yfinance as yf
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os

from Scripts.stock_data_fetcher import fetch_stock_data, get_nyse_symbols, record_stock_data

if __name__ == "__main__":
    alpha_vantage_api_key = 'Y439VIMJJTNWCSXE'  # Replace with your Alpha Vantage API key

    fortune_500_symbols = get_fortune_500_symbols()
    output_directory = 'stock_data'
    os.makedirs(output_directory, exist_ok=True)

    record_stock_data(alpha_vantage_api_key, fortune_500_symbols, output_directory)

    nyse_symbols = get_nyse_symbols(alpha_vantage_api_key)
    record_stock_data(alpha_vantage_api_key, nyse_symbols, output_directory)
