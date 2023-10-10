import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def get_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    tables = pd.read_html(url, header=0)
    df = tables[0]
    tickers = df['Symbol'].tolist()
    return tickers

def sort_by_price_ratio_and_pe(stock_list, limit=10):
    stock_data = []

    for stock in stock_list:
        ticker = yf.Ticker(stock)
        hist_data = ticker.history(period="max")
        
        if not hist_data.empty:
            average_price = hist_data['Close'].mean()
            current_price = hist_data['Close'].iloc[-1]
            pe_ratio = ticker.info.get("trailingPE", None)

            if current_price != 0:
                price_ratio = average_price / current_price
                stock_data.append((stock, price_ratio, pe_ratio))

    # Sort by price ratio first and then by P/E ratio
    sorted_stocks = sorted(stock_data, key=lambda x: (x[1], x[2]))[:limit]
    return [item[0] for item in sorted_stocks]  # Return just the tickers

def plot_stock_prices(stock_list, start_date, end_date):
    plt.figure(figsize=(15, 7))

    for stock in stock_list:
        ticker = yf.Ticker(stock)
        hist_data = ticker.history(start=start_date, end=end_date)
        plt.plot(hist_data['Close'], label=stock)

    plt.title("Stock Prices Over Time")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.grid(True)
    plt.show()

# Fetch all S&P 500 stocks
all_stocks = get_sp500_tickers()

# Sort them by price ratio and then by P/E ratio, and get the top 10
sorted_stocks = sort_by_price_ratio_and_pe(all_stocks, limit=10)

# Define date range for the plot
start_date = "2022-01-01"
end_date = "2023-10-06"

# Plot their prices over time
plot_stock_prices(sorted_stocks, start_date, end_date)
