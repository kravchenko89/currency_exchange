# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
from twilio.rest import Client

account_sid = 'AC828aa2cb7dea75182ab4409374ce99a4'
auth_token = '9e5440a25e0b61534e52fdcde6c792ff'

client = Client(account_sid, auth_token)

client.messages.create(
    body='hello',
    from_='+17066757210',
    to='+380934119141'
)
