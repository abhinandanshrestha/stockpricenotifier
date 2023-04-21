from flask import Flask, render_template,request
import yfinance as yf
import time

app = Flask(__name__)

@app.route('/')
def index():
    gspc = yf.Ticker("^GSPC")
    # gspc=yf.Ticker("MSFT")
    info = gspc.info
    history = gspc.history(period="1mo")
    print(info)
    return render_template('index.html',info=info,history=history)

# handle form
@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    ticker_symbol = request.form['tickerSymbol']
    pd = request.form['period']

    checkFrequency = request.form['checkFrequency']
    ask_threshold=request.form['ask']
    bid_threshold=request.form['bid']

    gspc_1 = yf.Ticker(ticker_symbol)
    # gspc=yf.Ticker("MSFT")
    info_1 = gspc_1.info
    history_1 = gspc_1.history(pd)
    
    # do something with the data
    # return 'Received form data: ticker symbol={}, period={}, freq={}, ask_threshold={}, bid_threshold={}'.format(ticker_symbol, period,checkFrequency,ask_threshold,bid_threshold)
    return render_template('index.html',info=info_1,history=history_1)

if __name__ == '__main__':
    app.run(debug=True)