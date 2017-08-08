import atexit
import unittest
import requests
from pact import Consumer, Provider

pact = Consumer('Translator').has_pact_with(Provider('Translate Service'), pact_dir='./pacts')

pact.start_service()

atexit.register(pact.stop_service)


class TranslateServiceContract(unittest.TestCase):

    mock_host="http://localhost:1234"

    def _request_helper(self, path):
        url = self.mock_host + path
        return requests.get(url)

    def test_get_translation_existing(self):
        path = '/translate/1'
        expected = {"en": "One", "ua": "Один"}
          
        (pact
         .given('translation for number 1')
         .upon_receiving('a request to get translation for number one')
         .with_request('get', path)
         .will_respond_with(200, body=expected))

        with pact:
          result = self._request_helper(path).json()
        
        self.assertEqual(result["en"], expected["en"])

    def test_get_translation_not_existing(self):
        path = '/translate/-1'
        expected = 404

        (pact
         .given('translation for number -1 doesn\'t exist')
         .upon_receiving('a request to get translation for number minus one')
         .with_request('get', path)
         .will_respond_with(expected))

        with pact:
          result = self._request_helper(path)

        self.assertEqual(result.status_code, expected)
