# Rules Engine

## System Design

### Architecture

![Architecture Diagram][diagram.png]

There are three microservices in this project. Each of the microservices have FlaskAPI endpoints and a connection can be made through approriate port number and host. More information about each microservice is given below.

1. Front End Service

The UI page offers the client to input details which is then routed to the Front end service. This service is the single point of contact from the UI.

The request is routed from the UI to '/process' endpoint with POST method in the Front End Service if the client enters details to either Creat, Update, Delete or Get rules. The Front End Service then routes the requests to the Rules DB Service.

The request is routed from the UI to '/evaluate' endpoint with POST method in the Front End Service If the client enters details to evaluate rules. The Front End Service then routes the requests to the Rules Engine Service.

2. Rules DB Service

The Rules DB Service can be accessed from the Front End Service on the '/rules' endpoint. It offers four option - Create, Update, Delete, Get.

To create a new rule, the Front End Service sends the rule data in json format to the Rules DB Service on the '/rules/create' endpoint. It checks if the rule name is duplicated. If not, a new rule is created. A rule id is assigned to the rule. This field is auto incremental.

To update a rule, the Front End Service sends the rule id and rule data in json format to the Rules DB Service on the '/rules/update/<rule_id>' endpoint. It checks if the rule id is valid and if the updated rule data is not duplicating an existing rule. On satisfying these two conditions, the rule is updated and reflected with a success message.

To get a rule, the Front End Service sends the rule id to the Rules DB Service on the '/rules/get/<rule_id>' endpoint. The service checks if the rule id exists and sends the rule details once the condition is satisfied.

To delete a rule, the Front End Service sends the rule id to the Rules DB Service on the '/rules/delete/<rule_id>' endpoint. It checks if the rule exists and deletes the rule corresponding to the rule id from the RulesFile table.

3. Rules Engine Service

The Rules Engine Service evaluates the incoming Customer object data given by the user on the UI page. It checks if the conditions provided in the incoming request satisfy the conditions corresponding to the rule name in the RulesFile table. If the conditions match, then the Customer proceeds to the 'accept_state'. Otherwise, the customer proceeds to the 'reject_state'.

In further iterations, multiple states can be added by storing them in a separate State object.

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
      - Enter the rules data in json format. Refer to the example below.
   - Update
      - Enter the rule id in the first input box.
      - Enter the entire rules data in json format. Refer to the example below.
   - Delete
      - Enter the rule id to delete the row corresponding to the rule id in the database.
   - Get
      - Enter the rule id to retrieve the row corresponding to the rule id in the database.
   - An example json formatted input data for 'Rule Data' field
      ```json
      {
         "name": "dummyRule", 
         "condition": [
         {
            "key": "dummy",
            "constraints": ">=",
            "value": 10
         }
         ],
         "action": "initial_state"
      }

2. Evaluate Rules form
   - This form allows the user to evaluate the rules for a Customer object
   - The user needs to provide this input in JSON format which consists of name, condition, and customer keys. The condition supports 'and' and 'or' condition. But, the current code only evaluates for '=' case. It can definitely be extended to evaluate other cases too.
   - An example input would look like this =>
      ```json
      {
         "name":"dummyRule",
         "condition":"dummy = 5",
         "customer": {
            "name": "John", 
            "state": "initial_state"
         }
      }
   - An example input for evaluating 'and' condition would look like this =>
      ```json
      {
         "name":"dummyRule",
         "condition":"dummy = 5 and dummy = 50",
         "customer": {
            "name": "John", 
            "state": "initial_state"
         }
      }
   - An example input for evaluating 'or' condition would look like this =>
      ```json
      {
         "name":"dummyRule",
         "condition":"dummy = 5 or dummy = 50",
         "customer": {
            "name": "John", 
            "state": "initial_state"
         }
      }
