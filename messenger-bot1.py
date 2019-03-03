## Python libraries that we need to import for our bot
from flask import Flask, request
from pymessenger.bot import Bot ## pymessenger is a Python wrapper for the Facebook Messenger API
from parse_html_try import *
from language_processing import determine_which_function

app = Flask(__name__) ## This is how we create an instance of the Flask class for our app

company_list = ['Apple', 'Google', 'Facebook', 'Microsoft']
interval = 180
recipient_id = None

_thread.start_new_thread(time_func, ())
def time_func():
    """
    Send the information about stock price every interval seconds
    :param interval: a tuple that is in the form of ('time length', 'time unit')
    :return: None
    """
    # Compute how many seconds are there in the interval
    # time_length = float(interval[0])
    # if interval[1] == str.capitalize("hours") or interval[1] == str.capitalize("hour"):
    #     interval = time_length * 3600
    # elif interval[1] == str.capitalize("minutes") or interval[1] == str.capitalize("minute"):
    #     interval = time_length * 60
    # else:
    #     interval = time_length
    global interval
    while True:
        time.sleep(interval)
        send_text = brief(company_list)
        send_message(recipient_id, send_text)


# ACCESS_TOKEN = 'EAAEjFjhdZB6EBAC3inioWY37BCmaS9Lo0dg4GXN51ZC97qZC5tFdgkjT2PoLkVOS3p9uKWgv8pwF8YHkEn00igCGCtxEXaWlSA8w9Hn4uqaI7YuydDLsjNHJhCFu5kWvyEcFHBniQqp5mWm5zhx1sUqOU7VosVSHmwlGA3CwwZDZD'
ACCESS_TOKEN = 'EAAEjFjhdZB6EBANq4AyxqPRkO0qAS1JtZAP2El0jzE0hxTaAZBUi1hnvZCaOIZAchZBFDZBLfUuFeK7CXyHx5Ut6GQrFHadkEZBdoVQuTXjXaZAK1L7sADTbEaAb6RY0QBZA94tuJl83ADlZA3MFmzDViv5hAHcz0T8yRJam4B4nNASgAZDZD'
VERIFY_TOKEN = 'fintech'
 ## Replace 'VERIFY_TOKEN' with your verify token
bot = Bot(ACCESS_TOKEN) ## Create an instance of the bot

def verify_fb_token(token_sent):
    ## Verifies that the token sent by Facebook matches the token sent locally
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

# Chooses a message to send to the user
def get_message_text():
    return "Hey, it looks like you're interested in HackRice! For more information, please visit http://hack.rice.edu"

## Send text message to recipient
def send_message(recipient_id1, response):
    bot.send_text_message(recipient_id1, response) ## Sends the 'response' parameter to the user
    return "Message sent"

## This endpoint will receive messages
@app.route("/", methods=['GET', 'POST'])
def receive_message():

    global company_list
    global recipient_id

    ## Handle GET requests
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token") ## Facebook requires a verify token when receiving messages
        return verify_fb_token(token_sent)

    ## Handle POST requests
    else:
       output = request.get_json() ## get whatever message a user sent the bot
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                recipient_id = message['sender']['id'] ## Facebook Messenger ID for user so we know where to send response back to

                ## If user sends text
                # HERE!!!!! WRITE YOUR SENT MESSAGE!!!!
                response_sent_text = message['message'].get('text')
                # send_message(recipient_id, response_sent_text)
                # send_message(recipient_id, 'Message received!')
                parse_tuple = determine_which_function(response_sent_text)
                control_sequence = parse_tuple[0]
                if control_sequence == 1:
                    company_list = parse_tuple[1]
                    send_message(recipient_id, 'All set!')
                elif control_sequence == 2:
                    interval = parse_tuple[1]
                    send_message(recipient_id, 'OK!')
                elif control_sequence == 3:
                    if parse_tuple[1] != None:
                        company_list = parse_tuple[1]
                    send_text = brief(company_list)
                    send_message(recipient_id, send_text)

    return 'OK'

def send_brief(company_list):
    global recipient_id
    send_text = brief(company_list)
    send_message(recipient_id, send_text)

## Ensures that the below code is only evaluated when the file is executed, and ignored if the file is imported
if __name__ == "__main__":
    app.run() ## Runs application
