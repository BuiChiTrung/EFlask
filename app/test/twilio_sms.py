from twilio.rest import Client

account_sid = 'AC679de3766e3c0c980f4355884d3ba3c5'
auth_token = '5b7e3ae704c9f9e67483be8b9d737d55'

client = Client(account_sid, auth_token)

message = client.messages.create(
                              body='Hello the gioi',
                              from_='+13254221982',
                              to='+840988864538'
                          )

print(message.sid)
