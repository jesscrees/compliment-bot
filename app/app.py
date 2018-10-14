import os
import nexmo


# NEXMO_API_KEY = os.environ['NEXMO_API_KEY']
# NEXMO_SECRET_KEY = os.environ['NEXMO_SECRET_KEY']
NEXMO_APPLICATION_ID = os.environ['NEXMO_APPLICATION_ID']
NEXMO_PRIVATE_KEY = os.environ['NEXMO_PRIVATE_KEY']
TEST_PHONE = os.environ['TEST_PHONE']

client = nexmo.Client(application_id=NEXMO_APPLICATION_ID, private_key=NEXMO_PRIVATE_KEY)

number_to_call = TEST_PHONE
 
# make a call
response = client.create_call({
    'to': [{'type': 'phone', 'number': number_to_call}],
    'from': {'type': 'phone', 'number': number_to_call},
    'answer_url': ['http://cb9df9b5.ngrok.io/answer']
})

print(response)

uuid = response['uuid']
# stream sybnthesized speech to a call
# ts_response = client.send_speech(uuid, text="Ain't nothing but a heartache")

# record
rec_response = client.get_recording(RECORDING_URL)

#Stop sending a synthesized speech message to a call
# response = client.stop_speech(uuid)
