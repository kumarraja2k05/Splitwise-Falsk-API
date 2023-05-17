from constants import IdConstants
import logging


user_id = IdConstants.user_id.value
group_id = IdConstants.group_id.value
expense_id = IdConstants.expense_id.value
balance_id = IdConstants.balance_id.value

class Helper:
    def inc_user_id(self):
        global user_id
        user_id = user_id + 1
        logging.debug("New user id is: ",user_id)
        return user_id
    
    def inc_group_id(self):
        global group_id
        group_id = group_id + 1
        logging.debug("New  group id is: ",group_id)
        return group_id
    
    def inc_expense_id(self):
        global expense_id
        expense_id = expense_id + 1
        logging.debug("New expense id is: ",expense_id)
        return expense_id
    
    def inc_balance_id(self):
        global balance_id
        balance_id = balance_id + 1
        logging.debug("New balance id is: ",balance_id)
        return balance_id
    
    def expense_management(amount,members):
        contribution = amount / len(members)
        borrowers_details = {}
        for member in members:
            borrowers_details[member] = contribution
        return borrowers_details  
