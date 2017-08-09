import json
import os

from flask import Flask, Response, request
from werkzeug.datastructures import Headers


HTTP_METHODS = ['GET', 'POST']

STATUS = {
    'not_found': Response(status=404),
    'ok': Response(status=200)
}

translations = {}

# FILE WITH TRANSLATIONS
file_path = os.path.dirname(__file__) + "/translations.json"

if (os.path.getsize(file_path) == 0):
    print(file_path + " file is empty!!!")

# APPLICATION HELPERS


def get_translation(status, number):
    with open(file_path) as file:
        translations = json.load(file)

    return Response(
        status=status,
        response=json.dumps(
            translations[number], ensure_ascii=False).encode('utf8'),
        headers=Headers([('Content-Type', 'application/json')]))

# STATES FOR TESTING


STATES = ['translation for number 1', 'no translation for number -1']


def prepare_state(state):

    translations_file = open(file_path, 'w')

    def write_to_file(translation):
        translation_dump = json.dumps(translation, ensure_ascii=False)
        translations_file.write(translation_dump)

    if (state == STATES[0]):
        write_to_file(
            {"1": {"de": 'eins', "en": 'one'}})

    elif (state == STATES[1]):
        write_to_file(
            {"4": {"de": "vier", "en": "fore"}})

    else:
        print("State {} is not implemented".format(state))

    translations_file.close()


# APPLICATION ENDPOINTS
app = Flask(__name__)


@app.route('/_pact/provider_states', methods=['GET', 'POST'])
def states():
    """ USAGE: python-verifier will send a request with the body:
               {consumer: 'Consumer name', states: ['a thing exists']}
               to this enpoint. One state at the time is allowed.
    """
    data = request.get_json()
    prepare_state(data["states"][0])

    return STATUS['ok']


@app.route('/translate/<number>', methods=['GET'])
def translate_number(number):
    try:
        return get_translation(200, number)
    except KeyError:
        return STATUS['not_found']


if __name__ == '__main__':
    app.run(port='5000')
