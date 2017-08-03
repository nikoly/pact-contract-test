import json

from flask import Flask, Response, request
from werkzeug.datastructures import Headers

HTTP_METHODS = ['GET', 'POST']

translations = {
    'consumer': {
        '1': Response(
            status=200,
            response=json.dumps({'ua': 'Один', 'en': 'One'}, ensure_ascii=False).encode('utf8'),
            headers=Headers([('Content-Type', 'application/json;charset=utf-8')])),
        '2': Response(
            status=200,
            response=json.dumps({'ua': 'Два', 'en': 'Two'}, ensure_ascii=False).encode('utf8'),
            headers=Headers([('Content-Type', 'application/json;charset=utf-8')]))
    }
}

status = {
    'not_found': Response(
            status=404
            )
}

app = Flask(__name__)

@app.route('/translate/<number>', methods=['GET'])
def translate_number(number):
    found = False
    for k,v in translations["consumer"].items():
        if k == number:
            found = True
            return v

    if not found:
        return status['not_found']


if __name__ == '__main__':
    app.run(port='5000')
