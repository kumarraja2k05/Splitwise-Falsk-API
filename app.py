from flask import Flask,request,jsonify
from helper.query import SQLAlchemyQuery
from helper.load_json import JsonLoader
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import logging
from constants import IdConstants
from flask_json_schema import JsonSchema

from db import db
import json
import uuid

app = Flask(__name__)
schema = JsonSchema(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///splitwise.db'
db.init_app(app)

logging.error(f"Secret Key is: {IdConstants.SECRET_KEY.value}")
app.config['JWT_SECRET_KEY'] = IdConstants.SECRET_KEY.value
jwt = JWTManager(app)

owner_details: dict = {}
expense_details: dict = {}
balance_details:dict = {}
groups:dict = {}
borrowers_details:dict = {}
groups_details:dict = {}

# Initialize the database before app starts
@app.before_first_request
def create_tables():
    db.create_all()

# This endpoint represents the homepage of the splitwise app
@app.route("/")
def home_page() -> str:
    return f"Welcome to SplitWise :-)"

# Here we are creating the owner account with respective details of the owner
@app.route("/login", methods=["POST"])
@schema.validate(JsonLoader().load_owner_json())
def login():
    global owner_details,access_token      # global is used for making the value of local variable accessible outside the method
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user_email = request.json.get("user_email", None)
    if username != "raja" or password != "raja":
        return {"msg": "Bad username or password"} ,401

    # adding the owner data in database
    try:
        SQLAlchemyQuery().add_owner(username, user_email, password)
        access_token = create_access_token(identity=username)
        logging.debug("access token recieved: ", access_token)
        return {"access_token":access_token, "status":"Successful"}
    except:
        return {"msg": "Error has occured"} , 400

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
    response = SQLAlchemyQuery().query_owner()
    if response == {}:
        return {"data":[],"status": "Successful"}
    return {**response,"status": "Successful"}

# Here we are creating new groups and adding the group members
@app.post("/groups")
@schema.validate(JsonLoader().load_group_json())
@jwt_required(refresh=False)
def create_group():
    global groups, groups_details
    group_description = request.json.get("group_description", None)
    group_members = request.json.get("group_members", None)
    group_name = request.json.get("group_name", None)
    try:
        SQLAlchemyQuery().add_group(group_name,group_members,group_description)
        response = SQLAlchemyQuery().query_group()
        groups_details = response["data"]
        return {**response, "status": "Successful"}
    except:
        return {"msg": "Error has occured"} , 400

# Here we are fetching the group details
@app.get("/groups")
@jwt_required(refresh=False)
def get_group_info() -> dict:
    global groups_details
    response = SQLAlchemyQuery().query_group()
    print("reponse: ",response)
    if response == {}:
        return {"data":[],"status": "Successful"}
    return {**response, "status": "Successful"}

# Here we are creating new expenses with their unique expense ID
@app.post("/expenses")
@schema.validate(JsonLoader().load_expense_json())
@jwt_required(refresh=False)
def add_expense() -> dict:
    global expense_details
    expense_amount = request.json.get("expense_amount", None)
    expense_name = request.json.get("expense_name", None)
    expense_paid_by = request.json.get("expense_paid_by", None)
    expense_settled = request.json.get("expense_settled", None)
    SQLAlchemyQuery().add_expense(expense_amount, expense_name, expense_paid_by, expense_settled, groups_details)
    response = SQLAlchemyQuery().query_expense()
    return {**response,"stauts": "Successful"}

# Here we are fetching the newly created expense
@app.get("/expenses")
@jwt_required(refresh=False)
def get_expense_details() -> dict:
   response = SQLAlchemyQuery().query_expense()
   if response == {}:
        return {"data":[],"status": "Successful"}
   return {**response, "stauts": "Successful"}

# If we want to fetch a particular expense form a bunch of expenses we can do it by using its unique expense Id
@app.get("/expenses/<int:expense_id>")
@jwt_required(refresh=False)
def get_expense_user(expense_id):
    global expense_details
    expense_id_list =  SQLAlchemyQuery().get_expense_list()
    try:
        if expense_id in expense_id_list:
            response = SQLAlchemyQuery().query_expense()
            return {**response,"status": "Successful"} ,200
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
    owner_id = SQLAlchemyQuery().get_owner_list()
    new_balance_details = SQLAlchemyQuery().add_balances(owner_id)
    response = SQLAlchemyQuery().query_balance()
    return {**response, "status":"Successfull"}


# Here we are updating a particular expense by using its expenseId as arguments
@app.put("/expenses/<int:expenseId>")
@jwt_required(refresh=False)
def update_expense(expenseId):
    global expense_details
    req = request.get_json()
    expense_id_list =  SQLAlchemyQuery().get_expense_list()
    if expenseId in expense_id_list:
        SQLAlchemyQuery().query_update_expense(req)
        return {"status":"Updated Successfuly"}
    return {"message":"Item Not found","status": "Failure"} , 404

# Delete a particular expense by using its expenseId as arguments
@app.delete("/expenses/<int:expenseId>")
@jwt_required(refresh=False)
def delete_expense(expenseId):
    global expense_details
    expense_id_list =  SQLAlchemyQuery().get_expense_list()
    if expenseId in expense_id_list:
        SQLAlchemyQuery().expense_delete_query()
        logging.debug(f'Expense {expenseId} is Deleted')
        return {"message":"Item Deleted", "status": "Successful"}
    else:
        logging.error(f'Expense_id: {expenseId} is not found')
        return {"message":"Item Not found"}, 404
    
# Update the owner details by using its ownerId as arguments
@app.put("/owner/<int:ownerId>")
@jwt_required(refresh=False)
def update_owner_details(ownerId):
    global owner_details
    req = request.get_json()
    owner_id_list = SQLAlchemyQuery().get_owner_id()
    if ownerId in owner_id_list:
        SQLAlchemyQuery().query_update_owner(req)
        return {"status":"Updated Successfuly"}
    
    return {"message":"Item Not found", "status": "Failure"} , 404

if __name__ == "__main__":
    app.run(debug=True)