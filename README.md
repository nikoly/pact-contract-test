 A use case for Pact framework, which allows doing contract testing. Contract testing with Pact allows running the tests faster than, e.g., integration or system tests.

[Pact](http://www.pact.io/)

# Before Start

To install working environment for Python and the project dependencies run the script

    ./setup.sh

and activate the venv.


# Sample service

There is a simple Python application in the app directory that has its own API. Right now it has only one method implemented - GET. To start the application run:

    python app/app.py

The app will be available at http://localhost:5000/.


# Creating the contract tests

Consumer creates a set of contract tests for HTTP API of the provider and runs them against mock service to generate JSON file - contract aka 'pact'. 

## Mock Service

1. [Install Pact Mock Service](https://github.com/pact-foundation/pact-mock_service)
    
    gem install pact-mock_service

2. Run the Service:

    pact-mock-service start


## Consumer Tests

1. Execute the tests (start pact-mock-service before):

    python -m unittest contract_tests/translate_service_contract.py

2. The contract will be generated and saved in **.pacts** dir if the run is successful.


# Provider Checks The Contract

## Verify the contract

The provider service has to be available on http://localhost:5000/.

To check the contract against the provider run:

    pact-verifier --provider-base-url=http://localhost:5000/ --pact-url=../../pacts/translate_service_contract.json


**pact-verifier** is installed with pact-python.

## Provider State

The provider implements states (fixture) that are defined by the consumer.

Consumer specifies the name of the state within a keyword 'given' and sends the contract to a provider. Once the provider gets the contract, he must implement the state before verifying that contracts. Import the state's implementation in pact_helper.py file.
