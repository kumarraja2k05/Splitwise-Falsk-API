from flask import Flask,request,jsonify
from helper.buissness_logic import Helper
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import logging
from constants import IdConstants
from flask_json_schema import JsonSchema

app = Flask(__name__)
schema = JsonSchema(app)

logging.error(f"Secret Key is: {IdConstants.SECRET_KEY.value}")
app.config['JWT_SECRET_KEY'] = IdConstants.SECRET_KEY.value
jwt = JWTManager(app)

owner_details: dict = {}
expense_details: dict = {}
balance_details:dict = {}
groups:dict = {}
borrowers_details:dict = {}

# This endpoint represents the homepage of the splitwise app
@app.route("/")
def home_page() -> str:
    return f"Welcome to SplitWise :-)"

# Here we are creating the owner account with respective details of the owner
@app.route("/login", methods=["POST"])
@schema.validate(Helper().load_owner_json())
def login():
    global owner_details,access_token      # global is used for making the value of local variable accessible outside the method
    req = request.get_json()
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "raja" or password != "raja":
        return {"msg": "Bad username or password"} ,401
    new_details = {**req,"balance_settled": True, "user_id": Helper().inc_user_id()}
    logging.debug(f'Response recieved from POST request is: {new_details}')
    owner_details = new_details
    access_token = create_access_token(identity=username)
    logging.debug("access token recieved: ", access_token)
    return {"access_token":access_token, "status":"Successful"}

@app.route("/logout", methods=["POST"])
def logout():
    access_token = create_access_token(identity=None)
    logging.debug("access token recieved: ", access_token)
    return {"status":"Succesful"}

# Here we are getting the owner details
# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.get("/owner")
@jwt_required(refresh=False)
def get_owner_details() -> dict:
    current_user = get_jwt_identity()
    return {"data":owner_details,"logged_in_as":current_user,"status": "Successful"}

# Here we are creating new groups and adding the group members
@app.post("/groups")
@schema.validate(Helper().load_group_json())
@jwt_required(refresh=False)
def create_group() -> dict:
    global groups, group_id
    req = request.get_json()
    logging.info('Getting response from POST method using request.get_json() library')
    new_details = {**req,"group_id":Helper().inc_group_id()}
    logging.debug(f'Response recieved from POST request is: {new_details}')
    groups = new_details
    return {"data":groups,"status": "Successful"}

# Here we are fetching the group details
@app.get("/groups")
@jwt_required(refresh=False)
def get_group_info() -> dict:
    return {"data": groups, "status": "Successful"}

# Here we are creating new expenses with their unique expense ID
@app.post("/expenses")
@schema.validate(Helper().load_expense_json())
@jwt_required(refresh=False)
def add_expense() -> dict:
    global expense_details, expense_id
    req = request.get_json()
    logging.warning('Here we have only considered equal contribution case')
    borrowers_details = Helper.expense_management(req["expense_amount"],groups["group_members"])
    logging.info(f'Group members details are fetched form the groups and they are considered as borrowers with values: {borrowers_details}')
    new_details = {**req,"expense_id": Helper().inc_expense_id(),"borrowers_details": borrowers_details, "group_id": groups["group_id"]}
    logging.debug(f'Response recieved from POST request is: {new_details}')
    expense_details = new_details
    return {"data: ":expense_details,"stauts": "Successful"}

# Here we are fetching the newly created expense
@app.get("/expenses")
@jwt_required(refresh=False)
def get_expense_details() -> dict:
    return {"data: ":expense_details, "stauts": "Successful"}

# If we want to fetch a particular expense form a bunch of expenses we can do it by using its unique expense Id
@app.get("/expenses/<int:expense_id>")
@jwt_required(refresh=False)
def get_expense_user(expense_id):
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

# Here we are fetching each user balnace with the owner
@app.get("/balances")
@jwt_required(refresh=False)
def get_balance_of_owner() -> dict:
    owner_id = owner_details["user_email"]
    new_balance_details = expense_details["borrowers_details"]
    if owner_details["user_email"] in list(expense_details["borrowers_details"].keys()):
        lender_id = expense_details["expense_paid_by"]
        new_balance_details[lender_id] = - new_balance_details.pop(owner_id)
        logging.debug(f'Owner is the borrower of {lender_id} with amount: {new_balance_details[lender_id]}')
    balance_details[owner_id] = new_balance_details
    return {"data": balance_details, "status":"Successfull"}


# Here we are updating a particular expense by using its expenseId as arguments
@app.put("/expenses/<int:expenseId>")
@jwt_required(refresh=False)
def update_expense(expenseId):
    global expense_details
    req = request.get_json()
    if expense_details["expense_id"] == expenseId:
        expense_details = req
        logging.debug(f'Response recieved from PUT request for updating the expense is: {expense_details}')
        return {"data": expense_details, "status":"Updated Successfuly"}
    return {"message":"Item Not found","status": "Failure"} , 404

# Delete a particular expense by using its expenseId as arguments
@app.delete("/expenses/<int:expenseId>")
@jwt_required(refresh=False)
def delete_expense(expenseId):
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
    
# Update the owner details by using its ownerId as arguments
@app.put("/owner/<int:ownerId>")
@jwt_required(refresh=False)
def update_owner_details(ownerId):
    global owner_details
    req = request.get_json()
    if owner_details["user_id"] == ownerId:
        owner_details = {**req,"user_id":ownerId}
        logging.debug(f'Response recieved from PUT request for updating owner details is: {owner_details}')
        return {"data": owner_details, "status":"Updated Successfuly"}
    
    return {"message":"Item Not found", "status": "Failure"} , 404

if __name__ == "__main__":
    app.run(debug=True)