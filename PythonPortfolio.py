'''
Name: Kavya Chichili
Date: 06/09/2024
Course: ICT-4370-1
Week 10: PORTFOLIO PROGRAMMING ASSIGNMENT
IMPROVING THE STOCK PROBLEM WITH ADDITIONAL FUNCTIONALITY
'''

import json
import pandas as pd
import datetime as dt
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Set up the main Tkinter window
root = tk.Tk()
root.title("Stock Data Visualization")

# Canvas and Labels for GUI
canvas = tk.Canvas(root, width=600, height=400, relief='raised')
canvas.pack()

label = tk.Label(root, text='Upload the CSV file to generate the stock graph', font=('helvetica', 14))
canvas.create_window(300, 25, window=label)

entry_label = tk.Label(root, text='Enter the Path:', font=('helvetica', 10))
canvas.create_window(300, 100, window=entry_label)

entry = tk.Entry(root)
canvas.create_window(300, 140, window=entry)

# Classes for stock data handling
class Stock:
    def __init__(self, symbol, date, open_price, high, low, close, volume):
        self.symbol = symbol
        self.date = date
        self.open = open_price
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
    
    def calculate_closing_value(self, num_shares):
        return round(float(self.close) * num_shares, 2)

def read_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        return pd.DataFrame(data, columns=['SYMBOL', 'NO_SHARES'])
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def read_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None

def get_file_path():
    return filedialog.askopenfilename()

def plot_graph(data, stock_data):
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=11))
    ax.xaxis.set_tick_params(rotation=80)
    left, right = dt.date(2015, 11, 9), dt.date(2018, 11, 10)
    plt.gca().set_xbound(left, right)
    
    for symbol in data['SYMBOL']:
        x_axis = [dt.datetime.strptime(stock['Date'], '%d-%b-%y').strftime('%d-%m-%y') for stock in stock_data if stock['Symbol'] == symbol]
        y_axis = [stock['Close'] for stock in stock_data if stock['Symbol'] == symbol]
        ax.plot(x_axis, y_axis, label=symbol)
    
    plt.xlabel('Date')
    plt.gca().invert_xaxis()
    plt.ylabel('Closing Price')
    ax.legend(data['SYMBOL'].tolist())
    plt.show()

def get_graph():
    csv_path = entry.get()
    csv_data = read_csv(csv_path)
    if csv_data is None:
        tk.Label(root, text='Invalid CSV file path', font=('helvetica', 10)).place(x=300, y=210)
        return

    json_path = 'c:/Users/Kavya Chichili/Downloads/AllStocks.json'
    stock_data = read_json(json_path)
    if stock_data is None:
        tk.Label(root, text='Invalid JSON file path', font=('helvetica', 10)).place(x=300, y=210)
        return

    try:
        stocks = {}
        for record in stock_data:
            symbol = record['Symbol']
            if symbol not in stocks:
                stocks[symbol] = []
            stock = Stock(symbol, record['Date'], record['Open'], record['High'], record['Low'], record['Close'], record['Volume'])
            num_shares = csv_data.loc[csv_data['SYMBOL'] == symbol, 'NO_SHARES'].values[0]
            closing_value = stock.calculate_closing_value(num_shares)
            stocks[symbol].append({'Date': record['Date'], 'Close': closing_value})
        
        plot_graph(csv_data, stocks)
    except Exception as e:
        print(f"Error processing data: {e}")
        tk.Label(root, text='Error processing data', font=('helvetica', 10)).place(x=300, y=210)

# Button to trigger graph generation
button = tk.Button(root, text='Submit', command=get_graph, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas.create_window(300, 180, window=button)

# Run the Tkinter event loop
root.mainloop()