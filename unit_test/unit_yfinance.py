import yfinance as yf

# gspc = yf.Ticker("^GSPC")
# gspc=yf.Ticker("^GSPC")
# print(gspc.info['currentPrice'])
# print(gspc.info)
# print(gspc.history(period="1y"))
# # set the bid price threshold here
# bid_threshold = 4200.0  # represents the maximum amount that a buyer is willing to pay for a security/stock

# # set the ask price
# ask_threshold = 4200.0  #  the minimum amount that a seller is willing to accept for the same security/stock

# if gspc.info['bid']>=bid_threshold or gspc.info['ask'] >=ask_threshold:
#     print(gspc.info['bid'],gspc.info['ask'])
# else:
#     print('Hasn\'t reached threshold')


gspc=yf.Ticker("MSFT")
print(gspc.info['currentPrice'])