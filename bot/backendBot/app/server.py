import flask
from flask import request, jsonify
from pylogflow import IntentMap, Agent
# Use Cloudant to create a Cloudant client using account
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey

# Copy this file to .env and replace the credentials with 
# your own before starting the app.

CLOUDANT_USERNAME="87a61610-7d39-4987-8aa7-5857c13e02b1-bluemix"
CLOUDANT_PASSWORD="2e36a4c5d2cac81aa643ccd2cc767aac8ff46b23fefea12d0c775c4f58c24575"
CLOUDANT_URL="https://87a61610-7d39-4987-8aa7-5857c13e02b1-bluemix:2e36a4c5d2cac81aa643ccd2cc767aac8ff46b23fefea12d0c775c4f58c24575@87a61610-7d39-4987-8aa7-5857c13e02b1-bluemix.cloudantnosqldb.appdomain.cloud"

## Un-comment and use either username+password or IAM apikey.
# NATURAL_LANGUAGE_UNDERSTANDING_USERNAME=<use natural language understanding username>
# NATURAL_LANGUAGE_UNDERSTANDING_PASSWORD=<use natural language understanding password>
NATURAL_LANGUAGE_UNDERSTANDING_IAM_APIKEY="7AGk8HyuLvEairikmsN1hkUwo9Xz7TzmB4ggaPxUOtvd"
NATURAL_LANGUAGE_UNDERSTANDING_URL="https://gateway.watsonplatform.net/natural-language-understanding/api"

## Un-comment and use either username+password or IAM apikey.
# TONE_ANALYZER_USERNAME=<use tone analyzer username>
# TONE_ANALYZER_PASSWORD=<use tone analyzer password>
TONE_ANALYZER_IAM_APIKEY="VLgifD_nXKGCh5i04m-ArF_6rp-Qo6MtExpwJrP-nvqB"
TONE_ANALYZER_URL="https://gateway.watsonplatform.net/tone-analyzer/api"

app = flask.Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/', methods=['POST'])
def home():
    # Send request as a json, result must be a dictionary
    result = intentMap.execute_intent(request.json)
    # Parse result into json format
    return jsonify(result)

def respuesta():
    # Set agent 
    agent = Agent()
    agent.add_message("Respuesta basica")
    return agent.get_response()

def consultarCloudant():
    # Authenticate using an IAM API key
    client = Cloudant(CLOUDANT_USERNAME, CLOUDANT_PASSWORD, url=CLOUDANT_URL, connect=True)

    session = client.session()
    print('Username: {0}'.format(session['userCtx']['name']))
    print('Databases: {0}'.format(client.all_dbs()))

    result_collection = Result(client["prueba"].all_docs, include_docs=True)
    print("Retrieved minimal document:\n{0}\n".format(result_collection[0]))
    # Disconnect from the server
    client.disconnect()

    return result_collection[0]
    

# Set up intent map
intentMap = IntentMap()
intentMap.add("IntentName", intentMethod)

# Set up server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)