# vaxtrack.py - quick Python script to confirm the appointment registration status and send an SMS message using Twilio
#
# Intended to be run routinely on a schedule and print to stdout - files / instructions for macOS included
#
# import os to pull twilio environment variables (see twilio.com/https://www.twilio.com/docs/sms/quickstart/python & https://www.twilio.com/docs/sms/quickstart/python#install-the-twilio-cli or instructions on preparing your environment for running this in a correct fashion.
#

import os
import requests
from twilio.rest import Client

#
# gets response header from harris countys api infra 
# 
hcphurl = requests.get('https://secureapp.hcphtx.org/vaxwebapi/api/PatientVaccine/checkifregistrationisavailable')
response = hcphurl.json()
availability = response['IsSuccess']
# sender is your twilio verified number
sender = "+##########"
# receiver is the destination number
receiver = "+##########"

#
# Twilio functions for SMS results 
# 
# funcs:
#
# twilio_send_test - sends a test SMS with text, emoji unicde, and url
#
# twilio_send_false - SMS output if the availability var has value of False
# 
# twilio_send_true_ SMS output if availablty var has value of "Not False"

def twilio_send_test():
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=("Test of SMS notification functionality for HCPH VaxTrack site - \U0001F60E - https://vacstrac.hctx.net/landing"),
                         from_= sender,
                         to= receiver,
                     )
    
    print(message.sid)

def twilio_send_false():
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=("No Appointments Available - \U0001F916"),
                         from_= sender,
                         to= receiver,
                     )
    
    print(message.sid)

def twilio_send_true():
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=("Appointments may be avaiable! - \U0001F60E - check https://vacstrac.hctx.net/landing"),
                        from_= sender,
                         to= receiver,
                     )
    
    print(message.sid)
#
# vax_check function verifies if header response has indicated it believes appointsments are avaible, prints to stdout, and fires appropraite Twilio func from above
#

def vax_check():
#  if the api says false call the correct twilio send functions
    if availability == False:
        txt  = "The API does not believe there are appointments available. Status: {}"
        print(txt.format(availability))
        twilio_send_false()
    else:
        txt = "The API believes there are appointments available! Status: {}"
        print(txt.format(availability))
        twilio_send_true()

#
# uncomment this to perform test SMS and verify Twilio CLI, Python Env, and scheduling are configured
#
# twilio_send_test()
vax_check()
