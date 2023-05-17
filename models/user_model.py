from db import db

class OwnerDetails(db.Model):
    __tablename__="user"
    user_id = db.Column(db.Integer, primary_key = True)  # table column id and declared it as a primary key
    username = db.Column(db.String(100), nullable = False)  # table column name with data type of String
    password = db.Column(db.String(150), nullable = False)
    user_email = db.Column(db.String(100), nullable= False)
    balance_settled = db.Column(db.Boolean, nullable= False)
    