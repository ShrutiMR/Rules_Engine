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

    def checkConditions(self, rule_condition, existing_condition):
        all_existing_conditions = []
        for cond in existing_condition:
            all_existing_conditions.append(list(cond.values()))
        # print('all_existing_conditions -- ', all_existing_conditions)
        existing_condition_op = all_existing_conditions[0][1]
        existing_condition_threshold = all_existing_conditions[0][2]

        all_rule_conditions = rule_condition.split("and ")
        all_rule_conditions = rule_condition.split("or ")
        print("all_rule_conditions -- ", all_rule_conditions)

        result_list = []
        for condition in all_rule_conditions:
            req_condition = condition.split(' ')
            rule_condition_op = req_condition[1]
            rule_condition_val = req_condition[2]

            print('rule_condition_op, rule_condition_val -- ', rule_condition_op, rule_condition_val)
            print('existing_condition_op, existing_condition_threshold -- ', existing_condition_op, existing_condition_threshold)

            if existing_condition_op == '>':
                result_list.append(int(rule_condition_val) > int(existing_condition_threshold))
            elif existing_condition_op == '>=':
                result_list.append(int(rule_condition_val) >= int(existing_condition_threshold))
            elif existing_condition_op == '<':
                result_list.append(int(rule_condition_val) < int(existing_condition_threshold))
            elif existing_condition_op == '<=':
                result_list.append(int(rule_condition_val) <= int(existing_condition_threshold))
            elif existing_condition_op == '==':
                result_list.append(int(rule_condition_val) == int(existing_condition_threshold))
            else:
                result_list.append(False)

        print('result_list -- ', result_list)
        if 'and' in rule_condition:
            return all(result_list) == True
        elif 'or' in rule_condition:
            return any(result_list) == True
        else:
            return result_list[0]