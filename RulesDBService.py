import json
import csv

class RulesDBService:
    def __init__(self) -> None:
        pass

    def createRule(self, json_input):
        format_rule = json.loads(json_input)

        csv_row = [format_rule["name"], format_rule["condition"], format_rule["action"]]

        csv_file_path = "rules_engine_db\RulesFile.csv"
        with open(csv_file_path, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(csv_row)

        print(f"The rule has been appended to {csv_file_path}.")

    def updateRule(self, json_input):
        pass

    def getRule(self, json_input):
        #Get the record from the rules_table
        pass

    def deleteRule(self, json_input):
        #Delete the record from the rules_table
        pass
