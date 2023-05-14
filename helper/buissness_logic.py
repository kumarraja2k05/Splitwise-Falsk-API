from constants import IdConstants
import logging
import json

user_id = IdConstants.user_id.value
group_id = IdConstants.group_id.value
expense_id = IdConstants.expense_id.value

class Helper:
    def inc_user_id(self):
        global user_id
        user_id = user_id + 1
        logging.debug("New user id is: ",user_id)
        return user_id
    
    def inc_group_id(self):
        global group_id
        group_id = group_id + 1
        logging.debug("New user id is: ",group_id)
        return group_id
    
    def inc_expense_id(self):
        global expense_id
        expense_id = expense_id + 1
        logging.debug("New user id is: ",expense_id)
        return expense_id
    
    def expense_management(amount,members):
        contribution = amount / len(members)
        borrowers_details = {}
        for member in members:
            borrowers_details[member] = contribution
        return borrowers_details
    
    def load_owner_json(self):
        with open('schemas\owner_schema.json') as file:
            data = json.load(file)
            return data
        
    def load_group_json(self):
        with open('schemas\group_schema.json') as file:
            data = json.load(file)
            return data
        
    def load_expense_json(self):
        with open('schemas\expense_schema.json') as file:
            data = json.load(file)
            return data
    
