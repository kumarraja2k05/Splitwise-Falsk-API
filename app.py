from flask import Flask,request
import uuid

app = Flask(__name__)

owner_details: dict = {}
expense_details: dict = {}
expense_id: None
is_balance_settled: bool
borrowers_id: list = []
borrowers_amount: list = []
borrowers_details:dict = {}
balance_details:dict = {}
groups:dict = {}

@app.route("/")
def home_page() -> str:
    # This endpoint represents the homepage of the splitwise app
    return f"Welcome to SplitWise :-)"


@app.post("/owner")
def add_owner_details() -> dict:
    # Here we are creating the owner account with respective details of the owner
    global owner_details
    req = request.get_json()
    balance_settled: bool = True
    new_details = {**req,"balance_settled": balance_settled, "user_id": uuid.uuid4().int}
    owner_details = new_details
    return {"data":owner_details, "status":"Successful"}

@app.get("/owner")
def get_owner_details() -> dict:
    # Here we are getting the owner details
    return {"data":owner_details, "status":"Successful"}

@app.post("/expenses")
def add_expense() -> dict:
    global expense_details
    req = request.get_json()
    expense_id:str = uuid.uuid4().hex
    new_details = {**req,"expense_id": expense_id}
    expense_details = new_details
    return {"data: ":expense_details,"stauts": "Successful"}

@app.get("/expenses")
def get_expense_details() -> dict:
    return {"data: ":expense_details, "stauts": "Successful"}

@app.get("/expenses/<string:expense_id>")
def get_expense_user(expense_id):
    try:
        if expense_details["expense_id"] == expense_id:
            return {"data":{"expense_id":expense_id,"borrowers_details":expense_details["borrowers_details"]}, "status": "Successful"}
    except:
        return {"meassage":"Item Not found", "stauts": "Failure"} , 404

@app.get("/balances")
def get_balance_of_owner() -> dict:
    owner_id = owner_details["user_email"]
    new_balance_details = expense_details["borrowers_details"]
    if owner_details["user_email"] in list(expense_details["borrowers_details"].keys()):
        lender_id = expense_details["expense_paid_by"]
        new_balance_details[lender_id] = new_balance_details.pop(owner_id)
    balance_details[owner_id] = new_balance_details
    return {"data": balance_details, "status":"Successfull"}


@app.post("/groups")
def create_group() -> dict:
    global groups
    req = request.get_json()
    group_id:int = uuid.uuid4().int
    expense_id:str = expense_details["expense_id"]
    new_details = {**req,"expense_id": expense_id,"group_id":group_id}
    groups = new_details
    return {"data":groups,"status": "Successful"}

@app.get("/groups")
def get_group_info() -> dict:
    return {"data": groups, "status": "Successful"}

@app.put("/expenses/<string:expenseId>")
def update_expense(expenseId):
    global expense_details
    req = request.get_json()
    if expense_details["expense_id"] == expenseId:
        expense_details = req
        return {"data": expense_details, "status":"Updated Successfuly"}
    return {"message":"Item Not found","status": "Failure"} , 404

@app.delete("/expenses/<string:expenseId>")
def delete_expense(expenseId):
    global expense_details
    try:
        if expense_details["expense_id"] == expenseId:
            del expense_details["expense_id"]
            return {"message":"Item Deleted", "status": "Successful"}
    except:
        return {"message":"Item Not found"},404
    
@app.put("/owner/<int:ownerId>")
def update_owner_details(ownerId):
    global owner_details
    req = request.get_json()
    print("\nowner details: ",owner_details)
    if owner_details["user_id"] == ownerId:
        owner_details = {**req,"user_id":ownerId}
        return {"data": owner_details, "status":"Updated Successfuly"}
    
    return {"message":"Item Not found", "status": "Failure"} , 404

if __name__ == "__main__":
    app.run(debug=True)