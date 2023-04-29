from flask import Flask, render_template,request,redirect,url_for
import yfinance as yf
import time
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import unit_test.config as config
from twilio.rest import Client

app = Flask(__name__)

# Function to handle sending email once currentPrice exceeds a threshold
def sendMail(email,reach):
    # Set up the email parameters
    sender = 'shtabhi@gmail.com'
    receiver = email
    password = config.PASSWORD
    subject = 'Email regarding increase in price of stock beyong your stated Threshold'

    # Create a message object
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = subject

    # Add the message body
    body = 'Current Price of your stock has reached '+ str(reach)
    message.attach(MIMEText(body, 'plain'))

    # Create the SMTP server
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()

    # Login to the SMTP server
    smtp_server.login(sender, password)

    # Send the email
    smtp_server.sendmail(sender, receiver, message.as_string())

    # Close the SMTP server
    smtp_server.quit()


# Function to handle sending sms once currentPrice exceeds a threshold
def sendSms(sms,reach):
    account_sid = config.account_sid
    auth_token = config.auth_token
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body="Stock Price Increased to "+str(reach),
                        from_='+15672293064',
                        to=sms
                    )

    print(message.sid+" Message sent")

# Route handlers
@app.route('/')
def index():
    # Define initial parameters for index page
    gspc = yf.Ticker("META")
    period_="5d"
    # gspc=yf.Ticker("MSFT")
    info = gspc.info
    history = gspc.history(period=period_)
    # print(info)
    return render_template('index.html',info=info,history=history)

@app.route('/indexpage', methods=['POST'])
def indexpage():
    ticker_symbol = request.form['tickerSymbol']
    period_ = request.form['period']
    return redirect(url_for('tickerData', symbol=ticker_symbol, period=period_))

@app.route('/<symbol>/<period>')
def tickerData(symbol, period):
    gspc = yf.Ticker(symbol)
    info = gspc.info
    history = gspc.history(period=period)
    return render_template('index.html', info=info, history=history)

# handle form
@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    ticker_symbol = request.form['tickerSymbol']
    checkFrequency = request.form['period']
    ask_threshold=request.form['ask']
    gspc_1 = yf.Ticker(ticker_symbol)
    sub=request.form['sub']
    sms=request.form['sms']
    email=request.form['email']
    thread = threading.Thread(target=background_thread,args=(gspc_1, checkFrequency, ask_threshold, sub, sms, email))
    thread.start()
    return render_template('success.html')

# Function to check if the price of stock has crossed the threshold
def check(gspc_1, ask_threshold, sub,sms,email):
    print(gspc_1.info['currentPrice'])
    if gspc_1.info['currentPrice'] > float(ask_threshold):
        print('Increased')
        if sub=='email':
            sendMail(email,gspc_1.info['currentPrice'])
        elif sub=='sms':
            sendSms(sms,gspc_1.info['currentPrice'])
        else:
            print('error')
    elif gspc_1.info['currentPrice'] < float(ask_threshold):
        print('decreased')
    else:
        print('stable')

def background_thread(gspc_1, checkFrequency, ask_threshold, sub, sms, email):
    while True:
        check(gspc_1, ask_threshold, sub,sms,email)
        time.sleep(int(checkFrequency))  # Call the function every t seconds

if __name__ == '__main__':
    app.run(debug=True,port=5002)     