# # Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC679de3766e3c0c980f4355884d3ba3c5'
auth_token = '5b7e3ae704c9f9e67483be8b9d737d55'
# ACCOUNT_SID=AC679de3766e3c0c980f4355884d3ba3c5
# AUTH_TOKEN=799bead51a964c8696489b2fb35b09d5
client = Client(account_sid, auth_token)

message = client.messages.create(
                              body='Chao youtuber',
                              from_='+13254221982',
                              to='+84326921446'
                          )

print(message.sid)
# import string
# import random

# def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))

# print(id_generator())
