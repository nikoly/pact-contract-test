This is a use case for Pact framework, that allows to do contract testing. Contract testing with Pact allows to run the tests faster than e.g., integration or system tests.

[Pact](http://www.pact.io/)

# Before Start

To install working environment for python and the project dependencies run the script

    ./setup.sh

and activate the venv.


# Sample service

There is a simple Python application in the app directory that has it's own API. Right now it has only one method implemented - GET. To start the application run:

    python app/app.py

The app will be available at http://localhost:5000/ .


# Creating the contract tests

Consumer creates a set of contract tests for HTTP API of the provider and runs them against mock service to generate JSON file - contract aka 'pact'. 

## Mock Service

1. [Install Pact Mock Service](https://github.com/pact-foundation/pact-mock_service)
    
    gem install pact-mock_service

2. Run the Service:

    pact-mock-service start


## Consumer Tests

1. Execute the tests (pact-mock-service has to be started before):

    python -m unittest device_service_pact.py

2. The contract will be generated and saved in **.pacts** dir if the run is successful.


# Provider Checks The Contract

## Verofy the contract

The provider service has to be available on http://localhost:5000/.

To check the contract against the provider run:

    pact-verifier --provider-base-url=http://localhost:5000/ --pact-url=../../pacts/frontend-translation_service.json


**pact-verifier** is installed with pact-python.

##Provider State

Additionally, provider can implement some states (fixture) that has to be run before the contract test. 

Consumer specifies the name of the state within a keyword 'given' and sends the contract to a provider. Once the provider gets the contract he must implement the state before verifying that contracts. The states must be imported in pact_helper.py file.
