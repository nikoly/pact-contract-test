import atexit
import unittest
import time
import requests
from pact import Consumer, Provider

pact = Consumer('Frontend').has_pact_with(
    Provider(
        'Translation Service'), pact_dir='./pacts')

pact.start_service()
atexit.register(pact.stop_service)



class GetDeviceContract(unittest.TestCase):
    def test_get_translation_existing(self):
        expected = {"en": "One", "ua": "Один"}
          
        (pact
         .given('translation for number one')
         .upon_receiving('a request to get translation for number one')
         .with_request('get', '/translate/1')
         .will_respond_with(200, body=expected))

        with pact:
          result = requests.get('http://localhost:1234/translate/1').json()
        
        self.assertEqual(result["en"], expected["en"])

    def test_get_translation_not_existing(self):
        expected = 404

        (pact
         .given('for number -1 doesn\'t exist')
         .upon_receiving('a request to get translation for number minus one')
         .with_request('get', '/translate/-1')
         .will_respond_with(404, body=''))

        with pact:
          result = requests.get('http://localhost:1234/translate/-1')

        self.assertEqual(result.status_code, expected)
