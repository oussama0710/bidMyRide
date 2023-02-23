from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB
from flask import flash
from flask_app.models import vehicle_model
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.cin = data['cin']
        self.password = data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.favourite_vehicles=[]

    @classmethod #register an account
    def register(cls, data):
        query = """
                INSERT INTO users (first_name, last_name, email, cin, password) 
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(cin)s, %(password)s)
                """
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod #! search user by email
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result= connectToMySQL(DB).query_db(query,data)
        if len(result)<1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls, data): #!READ
        query="SELECT * FROM users WHERE id=%(id)s;"
        result= connectToMySQL(DB).query_db(query,data)
        if len(result) <1:
            return False
        return cls(result[0])
    
    @classmethod #! Update profile
    def update_profile(cls, data):
        query = """UPDATE users SET first_name=%(first_name)s,
                last_name=%(last_name)s,email=%(email)s,cin=%(cin)s,password=%(password)s
                WHERE id=%(id)s;"""
        result= connectToMySQL(DB).query_db(query,data)
        if len(result)<1:
            return False
        return cls(result[0])
    
    @classmethod
    def add_favorite(cls,data):
        query = "INSERT INTO favourites (user_id,vehicle_id) VALUES (%(user_id)s,%(vehicle_id)s);"
        return connectToMySQL(DB).query_db(query,data)
    @classmethod
    def get_one_by_id(cls,data):
        query = """SELECT * FROM users 
        LEFT JOIN favourites ON users.id = favourites.user_id 
        LEFT JOIN vehicles ON vehicles.id = favourites.vehicle_id 
        WHERE users.id = %(id)s;
                """
        results = connectToMySQL(DB).query_db(query,data)

        user = cls(results[0])
        print("**************",results,"********************")
        for row in results:
            if row['authors.id'] == None:
                break
            data = {
                    "id":row["vehicles.id"],
                    "admin_id":row["admin_id"],
                    "product_type":row["product_type"],
                    "mileage":row["mileage"],
                    "age":row["age"],
                    "transmission":row["transmission"],
                    "fuel_type":row["fuel_type"],
                    "power":row["power"],
                    "seats":row["seats"],
                    "vehicle_name":row["vehicle_name"],
                    "description":row["description"],
                    "photos":row["photos"],
                    "start_price":row["start_price"],
                    "auction_start_date":row["auction_start_date"],
                    "auction_last_date":row["auction_last_date"],
                    "created_at":row["created_at"],
                    "uptated_at":data["uptated_at"]
            }
            user.favourite_vehicles.append(vehicle_model.Vehicle(data))
            print("************111**",user,"********************")
        return user


    @classmethod
    def unfavorited_authors(cls,data):
        query = "SELECT * FROM users WHERE users.id NOT IN ( SELECT user_id FROM favourites WHERE vehicle_id = %(id)s );"
        users = []
        results = connectToMySQL(DB).query_db(query,data)
        for row in results:
            users.append(cls(row))
        return users


    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['first_name'])<2:
            is_valid = False
            flash("Invalid first name, must be greater than 2 characters!", "first_name")
        if len(data['last_name'])<2:
            is_valid = False
            flash("Invalid last name, must be greater than 2 characters!", "last_name")
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", "email")
            is_valid = False
        elif User.get_by_email({'email': data['email']}):
            is_valid = False
            flash("email address already exists!", "email")
        if  len(data['cin'])!=8:
            flash("Invalid cin code!", "cin")
            is_valid = False
        if len(data['password'])<8:
            is_valid = False
            flash("Invalid password, must be greater than 8 characters!", "password")
        elif data['password']!=data['confirm_password']:
            flash("Password and confirm_password must match!", "confirm_password")
            is_valid = False
        return is_valid
    
    