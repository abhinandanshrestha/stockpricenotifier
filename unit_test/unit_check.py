import time
import yfinance as yf

gspc=yf.Ticker("^GSPC")

# # set the bid price threshold here
bid_threshold = 4109.96 # represents the maximum amount that a buyer is willing to pay for a security/stock

# set the ask price
ask_threshold = 4152.08  #  the minimum amount that a seller is willing to accept for the same security/stock

def check(gspc,ask_threshold):
    if gspc.info['ask'] > float(ask_threshold):
        print('Increased')
    elif gspc.info['ask'] < float(ask_threshold):
        print('decreased')
    else:
        print('stable')

def background_thread():
    while True:
        check(gspc,ask_threshold)
        time.sleep(60)  # Call the function every 60 seconds

background_thread()