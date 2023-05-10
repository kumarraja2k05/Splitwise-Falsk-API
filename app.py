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
    new_details = {**req,"balance_settled": balance_settled}
    owner_details = new_details
    return {"data":owner_details, "status":"Successful"}

@app.get("/owner")
def get_owner_details() -> dict:
    # Here we are getting the owner details
    return {"data":owner_details, "status":"Successful"}

@app.post("/expenses")
def add_expense() -> dict:
    expense_details["expense_name"] = "groceries"
    expense_details["expense_id"] = uuid.uuid4().hex
    expense_details["expense_paid_by"] = input("Enter the paying user email Id: ")
    expense_details["expense_amount"] = int(input("Enter the amount details: "))
    expense_details["expense_settled"] = True if int(input("Enter 0 for not settled \nEnter 1 for settled: \n")) else False
    borrowers_count: int = int(input("Enter the number of borrowers: "))
    for i in range(borrowers_count):
        borrowers_id.append(input("Enter the borrowers emaild id: "))
        if borrowers_id[i] == owner_details["user_email"]:
            borrowers_amount.append(-int(input(f"Enter the {borrowers_id[i]} amount: ")))
        else:
            borrowers_amount.append(int(input(f"Enter the {borrowers_id[i]} amount: ")))
        borrowers_details[borrowers_id[i]] = borrowers_amount[i]
    expense_details["borrowers_details"] = borrowers_details
    return {"data: ":expense_details,"stauts": "Successful"}

@app.get("/expenses")
def get_expense_details() -> dict:
    return {"data: ":expense_details, "stauts": "Successful"}

@app.get("/expenses/<string:expense_id>")
def get_expense_user(expense_id):
    if expense_details["expense_id"] == expense_id:
        return {"data":{"expense_id":expense_id,"borrowers_details":expense_details["borrowers_details"]}, "status": "Successful"}
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
    groups["group_name"] = input("Enter the group name: ")
    groups["group_id"] = uuid.uuid4().int
    groups["group_description"] = input("Enter the info for the new group: ")
    groups["expense_id"] = expense_details["expense_id"]
    group_member_count = int(input("Enter the group member count: "))
    groups["group_members"] = list(input("Enter the email id of that user: ") for i in range(group_member_count))
    return {"data":groups,"status": "Successful"}

@app.get("/groups")
def get_group_info() -> dict:
    return {"Group Info": groups}

@app.put("/expenses/<string:expenseId>")
def update_expense(expenseId):
    if expense_details["expense_id"] == expenseId:
        expense_details["expense_amount"] = int(input("Enter the new amount to be adjusted: "))
        if expense_details["expense_settled"] == False:
            if input("Do you want to settle the expenses press y or else n: ").lower() == "y":
                expense_details["expense_settled"] = True
        return {"data": expense_details, "status":"Updated Successfuly"}
    return {"message":"Item Not found","status": "Failure"} , 404

@app.delete("/expenses/<string:expenseId>")
def delete_expense(expenseId):
    # print("********* ",expense_details["expense_id"])
    # if expense_details["expense_id"] == expenseId:
    try:
        print("\nReached delete\n")
        expense_details = {}
        return {"message":"Item Deleted"}
    except KeyError:
        return {"message":"Item Not found"},404
    
@app.put("/owner/<string:ownerId>")
def update_owner_details(ownerId):
    if owner_details["user_email"] == ownerId:
        print("\nReached update owner\n")
        owner_details["user_name"] = input("Enter the new username: ")
        return {"data": owner_details, "status":"Updated Successfuly"}
    
    return {"message":"Item Not found", "status": "Failure"} , 404

if __name__ == "__main__":
    app.run(debug=True)