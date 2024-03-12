# Rules Engine

## System Design


There are three microservices in this project. Each of the microservices have FlaskAPI endpoints and a connection can be made through approriate port number and host. More information about each microservice is given below.

1. Front End Service

The UI page offers the client to input details which is then routed to the Front end service. This service is the single point of contact from the UI.

The request is routed from the UI to '/process' endpoint with POST method in the Front End Service if the client enters details to either Creat, Update, Delete or Get rules. The Front End Service then routes the requests to the Rules DB Service.

The request is routed from the UI to '/evaluate' endpoint with POST method in the Front End Service If the client enters details to evaluate rules. The Front End Service then routes the requests to the Rules Engine Service.

2. Rules DB Service



3. Rules Engine Service



## Setup Instructions

1. Clone the repository in your local.
2. Run the three services - FrontEndService, RulesDBService, RulesEngineService in three seperate CLI(CommandLine Interface).
3. Open a new window and enter - "http://127.0.0.1:9000/process" or you can also open the index.html file from templates
4. To run the test files, open a new CLI and change the directory to the root folder.
   - Enter this command for testing RulesDBService - python -m unittest tests.RulesDBServiceTest
   - Enter this command for testing RulesEngineService - python -m unittest tests.RulesEngineServiceTest

## Usage Guide

The UI has two forms -

1. Input Rules form
   - This form allows the user to create/update/get/delete any of the rules in the database.
   - Create
      - 
   - Update
      - Enter the rule id in the first input box.
      - Enter the other details in json format
   - Delete
      - Enter the rule id to delete the row corresponding to the rule id in the database.
   - Get
      - Enter the rule id to retrieve the row corresponding to the rule id in the database.

2. Evaluate Rules form
   - This form allows the user to evaluate the rules for a Customer object
   - The user needs to provide this input in JSON format.
   - An example input would look like this -
      {
         "name":"incomeRule", 
         "income":5000, 
         "customer": 
            {
               "name": "John", 
               "state": "initial_state"
            }
      }
