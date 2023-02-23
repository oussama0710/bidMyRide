from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB
from flask import flash
from flask_app.models import vehicle_model
from flask_app.models import user_model
class Bid:
    def __init__(self,data):
        self.vehichle_id=data["vehichle_id"]
        self.user_id=data["user_id"]
        self.bid_price=data["bid_price"]
        self.created_at=["created_at"]
        self.updated_at=["updated_at"]
    @classmethod
    def add_bidding(cls,data):
        query = """
                INSERT INTO bidding (vehichle_id, user_id, bid_price) 
                VALUES (%(vehichle_id)s, %(user_id)s, %(bid_price)s)
                """
        return connectToMySQL(DB).query_db(query, data)
    @classmethod
    def show_bidding(cls,data):
        query = """
                SELECT * FROM bidding 
                LEFT JOIN vehicles ON vehichle_id=bidding.vehichle_id
                LEFT JOIN users ON user_id=bidding.user_id
                WHERE users.id=%(id)s;
                """
        result= connectToMySQL(DB).query_db(query, data)
        bid=cls(result[0])
        for row in result:
            # if row['authors.id'] == None:
            #     break
            data = {
                    "id":row["vehicles.id"],
                    "admin_id":row["admin_id"],
                    "product_type":row["product_type"],
                    "mileage":row["mileage"],
                    "age":row["age"],
                    "transmission":row["transmission"],
            }