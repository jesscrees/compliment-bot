from app import verify

import nexmo
import requests
import logging
import os

from flask import Flask, session, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

NEXMO_APPLICATION_ID = os.environ['NEXMO_APPLICATION_ID']
NEXMO_PRIVATE_KEY = os.environ['NEXMO_PRIVATE_KEY']
TEST_PHONE = os.environ['TEST_PHONE']
number_to_call = TEST_PHONE

app.secret_key = os.environ['FLASK_SECRET_KEY']

client = nexmo.Client(application_id=NEXMO_APPLICATION_ID, private_key=NEXMO_PRIVATE_KEY)

@app.route('/health')
def health_check():
    return 200

@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    # Get phone number from form
    number_response = request.json['form_response']['answers'][0]['text']

    # Send verification code to phone number and get request id
    request_id = verify.send_verification(number_response)
    request_id_dict = {number_response: request_id}
    session['request_id_dict'] = request_id_dict
    
    print(request_id, number_response)

    return redirect(url_for('verification_code'))


@app.route('/verification_code', methods=['GET', 'POST'])
def verification_code():

    # Get form response
    code_response = request.json['form_response']['answers'][0]['text']
    phone_number_param = request.json['form_response']['hidden']['phone']


    # Get the request id from the file for this phone number
    request_id_dict = session.get('request_id_dict', None)
    request_id = request_id_dict[phone_number_param]
    print(request_id, phone_number_param)

    verification_status = verify.check_verification(request_id, code_response)
    if verification_status == "0":
        verify.store_number(phone_number_param)

    return "You're playing telephone"


@app.route('/calls', methods=['GET', 'POST'])
def calls():
    print('you are at the calls endpoint good job')
    response = client.create_call({
        'to': [{'type': 'phone', 'number': number_to_call}],
        'from': {'type': 'phone', 'number': number_to_call},
        'answer_url': [request.host_url+ 'answer']
    })

    return jsonify(response)

compliment1 = "<speak><break strength='weak' />There may not be many pandas left , but at least <prosody rate='slow'>we still have you.</prosody></speak>"

@app.route('/answer', methods=['GET', 'POST'])
def answer():
    print('HEY HEY HEY you got to the answer endpoint!')
    # talk to them
    ncco = [
                {
                    "action": "talk",
                    "voiceName": "Nicole",
                    "text": compliment1
                }
            ]

    return jsonify(ncco)

if __name__ == '__main__':
    app.run(port=8080)