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
        return requests.get(self.mock_host + path)

    def test_get_translation_existing(self):
        path = '/translate/1'
        expected_body = {"en": "one", "de": "eins"}
        expected_status = 200
          
        (pact
         .given('translation for number 1')
         .upon_receiving('a request to get translation for 1')
         .with_request('get', path)
         .will_respond_with(expected_status, body=expected_body))

        with pact:
          resp = self._request_helper(path)
        
        self.assertEqual(resp.status_code, expected_status)
        self.assertEqual(resp.json(), expected_body)

    def test_get_translation_not_existing(self):
        path = '/translate/-1'
        expected_status = 404

        (pact
         .given('no translation for number -1')
         .upon_receiving('a request to get translation for -1')
         .with_request('get', path)
         .will_respond_with(expected_status))

        with pact:
          resp = self._request_helper(path)

        self.assertEqual(resp.status_code, expected_status)
