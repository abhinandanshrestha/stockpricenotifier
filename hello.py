from flask import Flask, render_template,request,redirect
import yfinance as yf
import time
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import unit_test.config as config
from twilio.rest import Client

app = Flask(__name__)

# Define initial parameters for index page
gspc = yf.Ticker("META")
period_="1mo"

# Define initial parameters for subscription
gspc_1 = yf.Ticker("MSFT")
checkFrequency=2
ask_threshold=99999
sub=''
email=''
sms=''

# Function to handle sending email once currentPrice exceeds a threshold
def sendMail():
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
    body = 'Current Price of your stock has reached '+ str(gspc_1.info['currentPrice'])
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
def sendSms():
    account_sid = config.account_sid
    auth_token = config.auth_token
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body="Stock Price Increased to ",
                        from_='+15672293064',
                        to=sms
                    )

    print(message.sid+" Message sent")

# Route handlers
@app.route('/')
def index():
    # gspc=yf.Ticker("MSFT")
    info = gspc.info
    history = gspc.history(period=period_)
    # print(info)
    return render_template('index.html',info=info,history=history)

@app.route('/indexpage', methods=['POST'])
def indexpage():
    ticker_symbol = request.form['tickerSymbol']
    global period_
    period_ = request.form['period']
    global gspc
    gspc = yf.Ticker(ticker_symbol)
    return redirect('/')

# handle form
@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    ticker_symbol = request.form['tickerSymbol']
    # period_ = request.form['period']

    global checkFrequency
    checkFrequency = request.form['period']
    print(int(checkFrequency))

    global ask_threshold
    ask_threshold=request.form['ask']

    global gspc_1
    gspc_1 = yf.Ticker(ticker_symbol)

    global sub
    sub=request.form['sub']

    global sms
    sms=request.form['sms']

    global email
    email=request.form['email']

    thread = threading.Thread(target=background_thread)
    thread.start()

    return 'Your Subscription has been accepted'

# Function to check if the price of stock has crossed the threshold
def check():
    if gspc_1.info['currentPrice'] > float(ask_threshold):
        print('Increased')
        if sub=='email':
            sendMail()
        elif sub=='sms':
            sendSms()
        else:
            print('error')
    elif gspc_1.info['currentPrice'] < float(ask_threshold):
        print('decreased')
    else:
        print('stable')

def background_thread():
    while True:
        check()
        time.sleep(int(checkFrequency))  # Call the function every t seconds

if __name__ == '__main__':
    app.run(debug=True)     