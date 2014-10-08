from flask import Flask, request, redirect
import twilio.twiml as twiml
 
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
    response = twiml.Response()
    with response.gather(numDigits=4, action="/gather") as gather:
        gather.say("Hello welcome to Phone Cosse! If you have a user account please enter it now.")
    return str(response)
 
@app.route('/gather', methods=['POST'])
def gather():
    response = twiml.Response()
    digits = request.form['Digits']
    if digits in userIds:
        with response.gather(numDigits=1, action="/agreeChangePhone") as gather: 
            # pull user ID and phone number here
            gather.say("Welcome " + userIds[digits] + "Your current telephone number is " + userPhones[digits] +". If you would like to change it please press 1. If not you can hang up now")
    else:
        with response.gather(numDigits=4, action="/gather") as gather:
            gather.say("Sorry that number is invalid. Please try again.")
    return str(response)
    
@app.route('/agreeChangePhone', methods=['POST'])
def agreeChangePhone():
    response = twiml.Response()
    digits = request.form['Digits']
    if digits == "1":
        with response.gather(numDigits=10, action="/gatherPhone") as gather: 
            gather.say("Please enter your 10 digit phone number now.")
    return str(response)
    
@app.route('/gatherPhone',methods=['POST'])
def gatherPhone(): 
    response = twiml.Response()
    digits = request.form['Digits']
    with response.gather(numDigits=2, action="/verifyPhone") as gather: 
        gather.say("You have just entered " + digits[0:3] + "-" + digits[3:6] + "-" + digits[6:10] + " as your new phone number. If this is correct please press 1. If this is incorrect please press 2 to try again.")
    return str(response)

@app.route('/verifyPhone',methods=['POST'])
def verifyPhone(): 
    response = twiml.Response()
    digits = request.form['Digits']
    if digits=="1": 
        # Update database here 
        response.say("Thank you your number has been changed successfully!")
    if digits=="2": 
        with response.gather(numDigits=10, action="/gatherPhone") as gather: 
            gather.say("Please enter your 10 digit phone number now.")
    return str(response)



"""
@app.route('/', methods=['GET','POST'])
def intro(): 
    resp = twiml.Response()
    with resp.gather(numDigits=4, action='/gather') as gatherId: 
        gather.say("Hello welcome to Phone Cosse! If you have a user account please enter it now.")
    return str(response)

@app.route('/gather', methods=['POST'])
def gather(): 
    resp = twiml.Response()
    digits = request.form['Digits']
    if digits in userIds: 
        resp.say("You are in our database")
    else: 
        resp.say("Sorry this number is not valid")
    return str(resp)


@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    response = twiml.Response()
    response.say("hello") 
    return str(response)
    
        
"""


if __name__ == "__main__":
    app.run(debug=True)
