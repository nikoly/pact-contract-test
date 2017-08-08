import json
import os

from flask import Flask, Response, request
from werkzeug.datastructures import Headers

# constants

HTTP_METHODS = ['GET', 'POST']

STATUS = {
    'not_found': Response(status=404),
    'ok': Response(status=200)
}

translations = {}

app = Flask(__name__)

# Application Data Store Setup

file_translations_path = os.path.dirname(__file__) + "/translations.json"
size = os.path.getsize(file_translations_path)

if (size > 0):
    with open(file_translations_path) as file:
        translations = json.load(file)
else:
    print(file_translations_path + " file is empty")


# Helpers

def create_response(status, trnsl_data):
    return Response(
            status=status,
            response=json.dumps(trnsl_data, ensure_ascii=False).encode('utf8'),
            headers=Headers([('Content-Type', 'application/json')]))


# Provider states for testing purposes

STATES = ['translation for number 1', 'translation for number -1 doesn\'t exist']

def prepare_state(state):

    translations_file = open(file_translations_path, 'w')

    def write_to_file(translation):
        translation_dump = json.dumps(translation, ensure_ascii=False)
        translations_file.write(translation_dump)

    if (state == 'translation for number 1'):
        write_to_file(
            {"1": {"ua": 'Один', "en": 'One'}})

    elif (state == 'translation for number -1 doesn\'t exist'):     
        write_to_file(
            {"153": {"ua": "Cто п'ятдесят три", "en": "One hundred fifty three"}})

    else:
        print("State {} is not implemented".format(state))

    translations_file.close()

    global translations

    with open(file_translations_path) as file:
        translations = json.load(file)


# Application

# - provider states, for testing purposes

@app.route('/_pact/provider_states', methods=['GET','POST'])
def states():
    """This endpoint is an external endpoint for testing purposes. It's an example how
    provider states can be implemented. 
    
    USAGE: python-verifier will send a request with the body:
           JSON body {consumer: 'Consumer name', states: ['a thing exists']}
           to this enpoint
    """ 
    data = request.get_json()
    prepare_state(data["states"][0])

    return STATUS['ok']  

@app.route('/_pact/provider_states/all', methods=['GET','POST'])
def all_states():
    """ Get available provider states """
    return create_response(200, STATES)

# - main functionality

@app.route('/translate/<number>', methods=['GET'])
def translate_number(number):
    try:
        return create_response(200, translations[number])
    except KeyError:
        return STATUS['not_found']


if __name__ == '__main__':
    app.run(port='5000')
