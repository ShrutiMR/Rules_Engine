import csv

class Utils:

    def getExistingRows(self, csv_file_path):
        existing_rows = []
        with open(csv_file_path, mode='r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            existing_rows = list(csv_reader)
        return existing_rows
    
    def checkIfRuleExists(self, existing_rows, rule_id=None, rule_name=None):
        req_row = 0
        rule_exists = False
        for i, row in enumerate(existing_rows):
            if rule_id and row[0] == rule_id:
                rule_exists = True
                req_row = i
                break
            elif rule_name and row[1] == rule_name:
                rule_exists = True
                req_row = i
                break

        return rule_exists, req_row

    def checkConditions(self, rule_condition, req_condition):
        req_condition = req_condition.split(' ')
        operator = req_condition[1]
        threshold = int(req_condition[2])

        if operator == '>':
            if rule_condition > threshold:
                return True
            else:
                return False
        elif operator == '>=':
            if rule_condition >= threshold:
                return True
            else:
                return False
        elif operator == '<':
            if rule_condition < threshold:
                return True
            else:
                return False
        elif operator == '<=':
            if rule_condition <= threshold:
                return True
            else:
                return False
        elif operator == '==':
            if rule_condition == threshold:
                return True
            else:
                return False
        
        return False