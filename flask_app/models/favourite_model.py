from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DB

class Favourite:
    def __init__(self,data):
        self.vehicle_id=data["vehicle_id"]
        self.user_id=data["user_id"]
        self.favorized=data["favorized"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
    @classmethod
    def get_one_by_id(cls,data):
        query = """SELECT * FROM favourites WHERE user_id=%(user_id)s AND vehicle_id=%(vehicle_id)s;"""
        result= connectToMySQL(DB).query_db(query,data)
        if (result==()):# if the user didn't add any 
            return result
        return cls(result[0])
    @classmethod
    def get_all(cls):
        query = """SELECT * FROM favourites WHERE user_id=%(user_id)s """
        return connectToMySQL(DB).query_db(query)