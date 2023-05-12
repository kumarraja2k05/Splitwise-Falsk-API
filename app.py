from flask import Flask,request
from helper.buissness_logic import Helper
import logging

app = Flask(__name__)

owner_details: dict = {}
expense_details: dict = {}
balance_details:dict = {}
groups:dict = {}
borrowers_details:dict = {}


@app.route("/")
def home_page() -> str:
    # This endpoint represents the homepage of the splitwise app
    return f"Welcome to SplitWise :-)"


@app.post("/owner")
def add_owner_details() -> dict:
    # Here we are creating the owner account with respective details of the owner
    global owner_details,user_id      # global is used for making the value of local variable accessible outside the method
    req = request.get_json()
    logging.info('Getting response from POST method using request.get_json() library')
    new_details = {**req,"balance_settled": True, "user_id": Helper.inc_user_id()}
    logging.debug(f'Response recieved from POST request is: {new_details}')
    owner_details = new_details
    return {"data":owner_details, "status":"Successful"}

@app.get("/owner")
def get_owner_details() -> dict:
    # Here we are getting the owner details
    return {"data":owner_details, "status":"Successful"}

@app.post("/groups")
def create_group() -> dict:
    # Here we are creating new groups and adding the group members
    global groups, group_id
    req = request.get_json()
    new_details = {**req,"group_id":Helper.inc_group_id()}
    logging.debug(f'Response recieved from POST request is: {new_details}')
    groups = new_details
    return {"data":groups,"status": "Successful"}

@app.get("/groups")
def get_group_info() -> dict:
    # Here we are fetching the group details
    return {"data": groups, "status": "Successful"}

@app.post("/expenses")
def add_expense() -> dict:
    # Here we are creating new expenses with their unique expense ID
    global expense_details, expense_id
    req = request.get_json()
    logging.warning('Here we have only considered equal contribution case')
    borrowers_details = Helper.expense_management(req["expense_amount"],groups["group_members"])
    logging.info(f'Group members details are fetched form the groups and they are considered as borrowers with values: {borrowers_details}')
    new_details = {**req,"expense_id": Helper.inc_expense_id(),"borrowers_details": borrowers_details, "group_id": groups["group_id"]}
    logging.debug(f'Response recieved from POST request is: {new_details}')
    expense_details = new_details
    return {"data: ":expense_details,"stauts": "Successful"}

@app.get("/expenses")
def get_expense_details() -> dict:
    # Here we are fetching the newly created expense
    return {"data: ":expense_details, "stauts": "Successful"}

@app.get("/expenses/<int:expense_id>")
def get_expense_user(expense_id):
    # If we want to fetch a particular expense form a bunch of expenses we can do it by using its unique expense Id
    global expense_details
    try:
        if expense_details["expense_id"] == expense_id:
            return {"data":{"expense_id":expense_id,"borrowers_details":expense_details["borrowers_details"]}, "status": "Successful"} ,200
        else: 
            logging.error(f'Expense_id: {expense_id} is not found')
            return {"meassage":"Item Not found", "stauts": "Failure"} , 404
    except:
        # Here we are handling the keyError which is occured when we are unable to find the associated key
        logging.error('Exception has occured')
        return {"meassage":"Item Not found", "stauts": "Failure"} , 404

@app.get("/balances")
def get_balance_of_owner() -> dict:
    # Here we are fetching each user balnace with the owner
    owner_id = owner_details["user_email"]
    new_balance_details = expense_details["borrowers_details"]
    if owner_details["user_email"] in list(expense_details["borrowers_details"].keys()):
        lender_id = expense_details["expense_paid_by"]
        new_balance_details[lender_id] = - new_balance_details.pop(owner_id)
        logging.debug(f'Owner is the borrower of {lender_id} with amount: {new_balance_details[lender_id]}')
    balance_details[owner_id] = new_balance_details
    return {"data": balance_details, "status":"Successfull"}


@app.put("/expenses/<int:expenseId>")
def update_expense(expenseId):
    # Here we are updating a particular expense by using its expenseId as arguments
    global expense_details
    req = request.get_json()
    if expense_details["expense_id"] == expenseId:
        expense_details = req
        logging.debug(f'Response recieved from PUT request for updating the expense is: {expense_details}')
        return {"data": expense_details, "status":"Updated Successfuly"}
    return {"message":"Item Not found","status": "Failure"} , 404

@app.delete("/expenses/<int:expenseId>")
def delete_expense(expenseId):
    # Delete a particular expense by using its expenseId as arguments
    global expense_details
    try:
        if expense_details["expense_id"] == expenseId:
            del expense_details["expense_id"]
            logging.debug(f'Expense {expense_details} is Deleted')
            return {"message":"Item Deleted", "status": "Successful"}
        else:
            logging.error(f'Expense_id: {expense_id} is not found')
            return {"message":"Item Not found"}, 404
    except:
        # We are handling the errors occured due to unable to find the expenseId
        logging.error('Exception has occured')
        return {"message":"Item Not found"}, 404
    
@app.put("/owner/<int:ownerId>")
def update_owner_details(ownerId):
    # Update the owner details by using its ownerId as arguments
    global owner_details
    req = request.get_json()
    if owner_details["user_id"] == ownerId:
        owner_details = {**req,"user_id":ownerId}
        logging.debug(f'Response recieved from PUT request for updating owner details is: {owner_details}')
        return {"data": owner_details, "status":"Updated Successfuly"}
    
    return {"message":"Item Not found", "status": "Failure"} , 404

if __name__ == "__main__":
    app.run(debug=True)