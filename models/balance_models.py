from db import db

class BalanceDetails(db.Model):
    __tablename__ = "balance"
    balance_id = db.Column(db.String(100),primary_key = True)
    owner_id = db.Column(db.String(100),nullable=False)  # table column name with data type of String
    balance = db.Column(db.JSON, nullable=False)