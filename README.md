## Setup Pact Example

This is an use case for Pact framework, that allows to do contract testing. Contract testing with Pact allows to run the tests faster than e.g., integration or system tests.

[Pact](http://www.pact.io/)


### As A Consumer Create and Run the Contract Tests

Consumer creates a set of contract tests for HTTP API of the provider and runs them against mock service to generate JSON file - contract aka 'pact'. 

1. [Install Pact Mock Service](https://github.com/pact-foundation/pact-mock_service)
    
    gem install pact-mock_service

2. Run the Service:

    pact-mock-service start

3. Create consumer pact tests

4. Execute the tests:

    python -m unittest device_service_pact.py

5. Notice generated json file - a contract for a provider


### As A Provider Run The Contract On A Provider Service

Once json contract file is ready it must be available to a Provider as a file or via the URL. Provider runs the tests against their service based on this contract.


1. Run Test Application

    There is a simple Python application app.py that has it's own API. Right now it has only one method implemented - GET. To start the application run:

        python app.py 

    it will be run on port: 5000

2. Run the contract tests on Provider

    There is a pact-verifier tool, that allows to run the contract against provider service:

    pact-verifier --provider-base-url=http://localhost:5000/ --pact-url=../../pacts/frontend-translation_service.json


### Provider State

	Additionally, provider can implement some states (fixture) that has to be run before the contract test. 

	Consumer specifies the name of the statement within a keyword 'given' and sends the json file to a provider. Once the provider gets the contract he must implement the statements before verifying that contracts. The statements must be imported in pact_helper.py file.
