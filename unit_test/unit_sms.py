from twilio.rest import Client
import config

account_sid = config.account_sid
auth_token = config.auth_token
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Stock Price Increased to ",
                     from_='+15672293064',
                     to='+9779868205040'
                 )

print(message.sid+" Message sent")