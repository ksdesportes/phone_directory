"""
    This is the backend for the phone directory application. 
    It uses Flask as the router and twilio as the phone voice interface. 
    The capabilities of this application are to: 
        (1) Allow the user to check their phone number in the database based on their user ID
        (2) Allow the user to update their phone number in the database based on their user ID
"""

from flask import Flask, request, redirect
from twilio import twiml
 
app = Flask(__name__)

userIds = {
    "4444":"Ben", 
    "1234":"Leah", 
    "0000":"Kayla", 
    "8888":"Payal"
}

userPhones = {
    "4444":"443-678-9999", 
    "1234":"410-777-8877", 
    "0000":"778-636-3322", 
    "8888":"909-776-8837"
}


@app.route('/', methods=['POST'])
def intro():
    """ 
    Landing page for this application. 
    Prompts the user for their ID 
    """
    response = twiml.Response()
    with response.gather(numDigits=4, action='/gatherId') as gather:
        gather.say("Hello welcome to Phone Cosse! If you have a user account please enter it now.")
    return str(response)
 
@app.route('/gatherId', methods=['POST'])
def gatherId():
    """
    Get the user ID. 
    Say current phone number. 
    Allow user to change phone number. 
    Redirects to /agreeChangePhone
    """
    response = twiml.Response()
    digits = request.form['Digits']
    if digits in userIds:
        with response.gather(numDigits=1, action='/agreeChangePhone') as gather: 
            # pull user ID and phone number here
            speech = "Welcome {}. Your current telephone number is {}.  If you would like to change it please press 1. If not you can hang up now.".format(userIds[digits],userPhones[digits])
            gather.say(speech)
    else:
        with response.gather(numDigits=4, action='/gatherId') as gather:
            gather.say("Sorry that number is invalid. Please try again.")
    return str(response)
    
@app.route('/agreeChangePhone', methods=['POST'])
def agreeChangePhone():
    """
    Route user to change their phone number if they pressed 1. 
    Redirects to /confirmPhone.
    """
    response = twiml.Response()
    digits = request.form['Digits']
    if digits == "1":
        with response.gather(numDigits=10, action='/confirmPhone') as gather: 
            gather.say("Please enter your 10 digit phone number now.")
    return str(response)
    
@app.route('/confirmPhone',methods=['POST'])
def confirmPhone(): 
    """
    Re-iterate the phone number that was entered by the user. 
    Prompt them to confirm whether or not it was correct. 
    """
    response = twiml.Response()
    digits = request.form['Digits']
    with response.gather(numDigits=2, action='/savePhone') as gather: 
        speech = "You have just entered {}-{}-{} as your new phone number. If this is correct please press 1. If this is incorrect please press 2 to try again.".format(digits[0:3],digits[3:6],digits[6:10]) 
        gather.say(speech)
    return str(response)

@app.route('/savePhone',methods=['POST'])
def savePhone(): 
    """
    Saves phone number if user confirms it was input correctly  
    Redirects to enter the phone number if it was not entered correctly. --> /confirmPhone
    """
    response = twiml.Response()
    digits = request.form['Digits']
    if digits == "1": 
        # Update database here 
        response.say("Thank you your number has been changed successfully!")
    if digits == "2": 
        with response.gather(numDigits=10, action='/confirmPhone') as gather: 
            gather.say("Please enter your 10 digit phone number now.")
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)