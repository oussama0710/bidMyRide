from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model
from flask_app import DB
class Vehicle:
    def __init__(self,data):
        self.id=data["id"]
        self.admin_id=data["admin_id"]
        self.product_type=data["product_type"]
        self.mileage=data["mileage"]
        self.age=data["age"]
        self.transmission=data["transmission"]
        self.fuel_type=data["fuel_type"]
        self.power=data["power"]
        self.seats=data["seats"]
        self.vehicle_name=data["vehicle_name"]
        self.description=data["description"]
        self.photos=data["photos"]
        self.start_price=data["start_price"]
        self.auction_start_date=data["auction_start_date"]
        self.auction_last_date=data["auction_last_date"]
        self.created_at=data["created_at"]
        self.uptated_at=data["uptated_at"]
        self.users_who_favorited=[]
    @classmethod
    def save_vehicle(cls,data):
        query="""
        INSERT INTO vehicles (admin_id,product_type,mileage,age,transmission,fuel_type,power,seats,vehicle_name,
        description,photos,start_price,auction_start_date,auction_last_date)
        VALUES (%(admin_id)s,%(prodect_type)s,%(mileage)s,%(age)s,%(transmission)s,%(fuel_type)s,%(power)s,%(seats)s,%(vehicle_name)s
        ,%(description)s,%(photos)s,%(start_price)s,%(auction_start_date)s,%(auction_last_date)s) ; 
        """
        return connectToMySQL(DB).query_db(query,data)
    @classmethod
    def get_all(cls):
        query = """SELECT * FROM vehicles;"""
        return connectToMySQL(DB).query_db(query)
    @classmethod
    def get_result(cls):
        query = """SELECT * FROM vehicles 
        WHERE product_type=%(vehicle_type)s 
        AND make=%(make)s
        ORDER BY start_price %(order)s ;
        """
        return connectToMySQL(DB).query_db(query)
    @classmethod
    def delete(cls, data):
        query = """DELETE FROM vehicles WHERE id = %(id)s;"""
        return connectToMySQL(DB).query_db(query,data)
    
    @classmethod
    def unfavorited_vehicles(cls,data):
        query = "SELECT * FROM vehicles WHERE vehicles.id NOT IN ( SELECT vehicle_id FROM favourites WHERE user_id = %(id)s );"
        results = connectToMySQL(DB).query_db(query,data)
        vehicles = []
        for row in results:
            vehicles.append(cls(row))
        print(vehicles)
        return vehicles
    
    @classmethod
    def get_by_id(cls,data):
        query = """SELECT * FROM vehicles 
        LEFT JOIN favourites ON vehicles.id = favourites.vehicle_id 
        LEFT JOIN users ON users.id = favourites.user_id 
        WHERE vehicles.id = %(id)s;"""
        
        results = connectToMySQL(DB).query_db(query,data)

        vehicle = cls(results[0])

        for row in results:
            """ if row['authors.id'] == None:
                break """
            data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "cin": row['cin'],
                "password": row['password'],
                "role": row['role'],
                "created_at": row['authors.created_at'],
                "updated_at": row['authors.updated_at']
            }
            vehicle.users_who_favorited.append(user_model.User(data))
        return vehicle
    @staticmethod 
    def validate_vehicle(data):
        is_valid = True
        if len(data['product_type'])==0:
            is_valid = False
            flash("You must select type!", "product_type")
        if len(data['mileage'])<2:
            is_valid = False
            flash("you must select mileage", "mileage")
        if len(data['age'])<1:
            is_valid = False
            flash("you must select age", "age")
        if len(data['transmission'])<1:
            is_valid = False
            flash("you must select transmission", "transmission")
        if len(data['fuel_type'])<1:
            is_valid = False
            flash("you must select fuel type", "fuel_type")	
        if len(data['power'])<1:
            is_valid = False
            flash("you must select power", "power")
        if len(data['seats'])<1:
            is_valid = False
            flash("you must select seats", "seats")
        if len(data['vehicle_name'])<4:
            is_valid = False
            flash("you must select vehicle name", "vehicle_name")
        if len(data['description'])<1:
            is_valid = False
            flash("you must select description", "description")
        if len(data['photos'])<1:
            is_valid = False
            flash("you must select photo", "photos")
        if len(data['start_price'])<1:
            is_valid = False
            flash("you must select start price", "start_price")
        if len(data['auction_start_date'])=="":
            is_valid = False
            flash("you must select auction start date", "auction_start_date")
        if len(data['auction_last_date'])==0:
            is_valid = False
            flash("you must select auction last date", "auction_last_date")
        return is_valid




