#import statements

class RulesTableOperations:
    def __init__(self) -> None:
        pass

    def createRule():
        #Insert the new record in the database

        #establish a connection with the database
        pass

    def updateRule():
        #Update the record in the database
        pass

    def getRule():
        #Get the record from the database
        pass

    def deleteRule():
        #Delete the record from the database
        pass

#accept input rules from user and the json input data
user_input = input('Do you want to create/update/read/delete/None any rules?')
user_input = user_input.lower()
json_input = ''
if user_input != 'none':
    json_input = input('Provide the rule in json format')

#create a Rules object
rule_input = RulesTableOperations()
if user_input == 'create':
    rule_input.createRule(json_input)
elif user_input == 'update':
    rule_input.updateRule(json_input)
elif user_input == 'delete':
    rule_input.deleteRule(json_input)
elif user_input == 'get':
    rule_input.getRule(json_input)

#accept input data from user
data_input = input('What rule do you want to execute?')

##call the rules engine for further process

#query the rule from the database and pass to the rule engine

#If success, execute action and return action message

#Else return the error message