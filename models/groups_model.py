from db import db

class GroupDetails(db.Model):
    __tablename__ = "groups"
    group_id = db.Column(db.Integer, primary_key = True)  # table column id and declared it as a primary key
    group_description = db.Column(db.String(1000), nullable = False)  # table column name with data type of String
    group_members = db.Column(db.JSON, nullable = False)
    group_name = db.Column(db.String(100), nullable= False)

    # expense_details = db.relationship('ExpenseDetails', backref='groups', lazy = True)
    # borrowers_details = db.relationship('ExpenseDetails', backref='borrower', lazy = True)
