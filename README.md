Sample project to set up contract testing for a smaple application using [pact](https://docs.pact.io), [python implementation](https://github.com/pact-foundation/pact-python). As a refference I use **pact-python** official repo [example](https://github.com/pact-foundation/pact-python/tree/master/e2e).

# Setup Python Environment

To install working environment for Python and the project dependencies run the script

 ```sh
 ./setup.sh
 ```

Please, follow instructions printed by the script by the end of execution.

# Sample Provider Service

The sample service `app/app.py` translates numbers to different languages. It has a HTTP API. The only endpoint `GET /translate/1` translates prime numbers to various languages `200 OK {"ua": "Один", "en": "One"}`. When there is no translation for a given number, it will respond with `404 Not found`.

To run the service on `http://localhost:5000/`:

 ```sh
 python app/app.py
 ```

# Contract tests

## Install tools

When the python environment is ready install **(1) pact** and **(2) pact mock service** (ruby is required). Mock service is needed to run the contract tests.

Install [pact-python](https://github.com/pact-foundation/pact-python):

 ```sh
 pip install pact-python
 ```

Install [pact mock service](https://github.com/pact-foundation/pact-mock_service):

 ```sh
 gem install pact-mock_service
 ```

Start the mock service on `http://localhost:1234`:
 ```sh
 pact-mock-service start
 ```

## Create and Run

In this example I use **unittest** to create the contract tests `contract_tests/translate_service_test.py`.
**given** is a specific [provider state](). The state should be implemented later by Provider. For example, if your test requires some data in the service provider data store.

Execute the contract tests:
 ```sh
 python -m unittest contract_tests/translate_service_test.py
 ```

The test will run against the **pact mock service**, which verifies if all requests in the tests were triggered. If successful, **pact mock service** will generate a pact file in JSON format `pacts/translator_translate-service.json`. The location of the dir where the pacts should be stored you setup in the test:

 ```python
 from pact import Consumer, Provider
 pact = Consumer('Translator').has_pact_with(Provider('Translate Service'), pact_dir='./pacts')
 ```

# Provider

## Implement Provider State

**pact-verifier** is installed with **pact-python**. It is a utility to verify the pact instructions against a real service provider. It needs to know where are provider states implemented `--provider-states-url`  and `--provider-states-setup-url`.
When **pact-verifier** reads the instructions and finds a **providerState** it makes a call to the URL provided in `--provider-states-setup-url` with a body:

    {consumer: <consumer_name>, states: [<state_name>]}

For some reason, **pact-verifier** requires `--provider-states-url` to be specified but doesn't use it.


I implemented **provider states** inside the sample application `app/app.py`. The provider state name can be passed by **pact-verifier** to `POST /_pact/provider_states/` with expected Body: `{consumer: ‘Translator’, states: [‘translation for number 1’]}` and the state will be executed to set up the state of the service.

 ## Verify a pact

 To verify a pact instructions run:

 ```sh
 pact-verifier --provider-base-url=http://localhost:5000/ --pact-url=pacts/translator-translate_service.json --provider-states-url=http://localhost:5000/_pact/provider_states/all --provider-states-setup-url=http://localhost:5000/_pact/provider_states
 ```

At the end, you should see a report printed to the command line output.
