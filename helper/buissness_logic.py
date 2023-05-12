from constants import IdConstants
import logging

user_id = IdConstants.user_id.value
group_id = IdConstants.group_id.value
expense_id = IdConstants.expense_id.value

class Helper:
    def inc_user_id():
        global user_id
        user_id = user_id + 1
        logging.debug("New user id is: ",user_id)
        return user_id
    
    def inc_group_id():
        global group_id
        group_id = group_id + 1
        logging.debug("New user id is: ",group_id)
        return group_id
    
    def inc_expense_id():
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
    
