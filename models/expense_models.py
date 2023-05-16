from db import db

class ExpenseDetails(db.Model):
    __tablename__ = "expense"
    expense_id = db.Column(db.Integer, primary_key = True)  # table column id and declared it as a primary key
    expense_amount = db.Column(db.Integer, nullable = False)
    expense_name = db.Column(db.String(100), nullable = False)  # table column name with data type of String
    expense_paid_by = db.Column(db.String(200), nullable = False)
    expense_settled = db.Column(db.Boolean, nullable= False)
    group_id = db.Column(db.Integer, nullable = False)
    borrowers_details = db.Column(db.JSON, nullable = False)
    # group_id = db.Column(db.Integer, db.ForeignKey("groups.group_id"), nullable = False)
    # borrowers_details = db.Column(db.JSON, db.ForeignKey("groups.group_members"), nullable = False)
