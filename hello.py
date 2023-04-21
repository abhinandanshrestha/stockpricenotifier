from flask import Flask, render_template,request
import yfinance as yf

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
    checkFrequency=period = request.form['checkFrequency']
    ask_threshold=request.form['ask']
    bid_threshold=request.form['bid']

    gspc = yf.Ticker(ticker_symbol)
    # gspc=yf.Ticker("MSFT")
    info = gspc.info
    history = gspc.history(pd)

    if gspc.info['bid']>=bid_threshold or gspc.info['ask'] >=ask_threshold:
        print(gspc.info['bid'],gspc.info['ask'])
    else:
        print('Hasn\'t reached threshold')
    
    # do something with the data
    # return 'Received form data: ticker symbol={}, period={}, freq={}, ask_threshold={}, bid_threshold={}'.format(ticker_symbol, period,checkFrequency,ask_threshold,bid_threshold)
    return render_template('index.html',info=info,history=history)

if __name__ == '__main__':
   app.run(debug=True)