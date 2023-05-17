from db import db
from models.user_model import OwnerDetails
from models.groups_model import GroupDetails
from models.expense_models import ExpenseDetails
from models.balance_models import BalanceDetails
from helper.buissness_logic import Helper
import logging

class SQLAlchemyQuery:
    owner_details: list = []
    def query_owner(self):
        global owner_details
        owner_details = OwnerDetails.query.all()
        logging.debug(f"owner details {owner_details} ")
        response = {"data":{"user_id": user.user_id,"username":user.username, "user_email":user.user_email, "balance_settled": user.balance_settled} for user in owner_details}
        return response

    def add_owner(self,username, user_email, password):
        owner = OwnerDetails(username = username, user_email = user_email, password = password, balance_settled = True, user_id = Helper().inc_user_id())
        db.session.add(owner)
        db.session.commit()

    def add_group(self, group_name, group_members, group_description):
        group_details = GroupDetails(group_id = Helper().inc_group_id(),group_name = group_name,group_members = group_members,group_description = group_description)
        db.session.add(group_details)
        db.session.commit()

    def query_group(self):
        groups = GroupDetails.query.all()
        response = {"data": {"group_id": group.group_id, "group_name": group.group_name, "group_description": group.group_description, "group_members": group.group_members} for group in groups}
        return response

    def add_expense(self, expense_amount, expense_name, expense_paid_by, expense_settled, groups_details):
        borrowers_details = Helper.expense_management(expense_amount, groups_details["group_members"])
        expense_details = ExpenseDetails(expense_id = Helper().inc_expense_id(), borrowers_details = borrowers_details, group_id = groups_details["group_id"],expense_name = expense_name, expense_paid_by = expense_paid_by, expense_settled = expense_settled, expense_amount = expense_amount)
        db.session.add(expense_details)
        db.session.commit()

    def query_expense(self):
        expense_details = ExpenseDetails.query.all()
        response = {"data": {"group_id": expense.group_id,"borrowers_details": expense.borrowers_details, "expense_name":expense.expense_name, "expense_paid_by": expense.expense_paid_by,"expense_settled": expense.expense_settled , "expense_amount": expense.expense_amount,"expense_id": expense.expense_id} for expense in expense_details}
        return response
    
    def get_expense_list(self):
        expense_details = ExpenseDetails.query.all()
        res = list(expense.expense_id for expense in expense_details)
        return res
    
    def get_specific_expense(self, expense_id):
        expense = ExpenseDetails.query.filter_by().first()
        response = {"data": {"group_id": expense.group_id,"borrowers_details": expense.borrowers_details, "expense_name":expense.expense_name, "expense_paid_by": expense.expense_paid_by,"expense_settled": expense.expense_settled , "expense_amount": expense.expense_amount,"expense_id": expense.expense_id}}
        logging.debug("\nexpense details: ",response) 
        return response
    
    def get_owner_list(self):
        owner_details = OwnerDetails.query.all()
        owner_email = list(owner.user_email for owner in owner_details)
        return owner_email
    
    def add_balances(self, owner_id):
        expense_details = ExpenseDetails.query.all()
        new_balance_details = list(expense for expense in expense_details)
        logging.debug(f"New Balance details is {new_balance_details}")
        if owner_id[0] in list(new_balance_details[0].borrowers_details.keys()):
            lender_id = new_balance_details[0].expense_paid_by
            logging.debug(f"\nlender id: {lender_id}")
            new_balance_details[0].borrowers_details[lender_id] = - new_balance_details[0].borrowers_details.pop(owner_id[0])
            logging.debug(f'Owner is the borrower of {lender_id} with amount: {new_balance_details[0].borrowers_details[lender_id]}')
        balance = BalanceDetails(balance_id = Helper().inc_balance_id() ,owner_id = owner_id[0], balance = new_balance_details[0].borrowers_details)
        db.session.add(balance)
        db.session.commit()

    def query_balance(self):
        balance_details = BalanceDetails.query.all()
        response = {"data": {"balance_details": bal.balance} for bal in balance_details}
        return response

    def query_update_expense(self, req):
        expense = ExpenseDetails(borrowers_details = req["borrowers_details"], group_id = req["group_id"],expense_name = req["expense_name"], expense_paid_by = req["expense_paid_by"], expense_settled = req["expense_settled"], expense_amount = req["expense_amount"])
        logging.debug(f'Response recieved from PUT request for updating the expense is: {expense}')
        db.session.add(expense)
        db.session.commit()

    def expense_delete_query(self):
        expense_res = ExpenseDetails.query.filter_by().first()
        db.session.delete(expense_res)
        db.session.commit()

    def query_update_owner(self, req):
        global owner_details
        logging.debug("\nowner_details: ", owner_details)
        owner = OwnerDetails(username = req["username"], user_email = req["user_email"], balance_settled = req["balance_settled"], password = owner_details[0].password)
        db.session.add(owner)
        db.session.commit()
        logging.debug(f'Response recieved from PUT request for updating owner details is: {owner}')

    def get_owner_id(self):
        owner_details = OwnerDetails.query.all()
        owner_id = list(owner.user_id for owner in owner_details)
        return owner_id