import yfinance as yf

gspc=yf.Ticker("META")
print(gspc.info['currentPrice'])