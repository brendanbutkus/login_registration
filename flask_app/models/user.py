from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

class User:
    def __init__(self,data):
        self.id = data['id']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def insert_user(cls,data):
        query = "INSERT INTO users (email,password) VALUES (%(email)s,%(password)s)"
        return connectToMySQL("users_db").query_db(query,data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s"
        user_db = connectToMySQL("users_db").query_db(query,data)

        if len(user_db) < 1:
            return False
        
        return cls(user_db[0])
    
    @staticmethod
    def validate_register(user):
        email_reg =  re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        is_valid = True
        if len(user["first_name"]) <= 3:
            flash("First name must be three characters")
            is_valid = False

        if len(user["last_name"]) <= 3:
            flash("Last name must be three characters")
            is_valid = False
        
        if not email_reg.match(user["email"]):
            flash("Invalid Email")
            is_valid = False
        
        if len(user["password"]) < 8:
            flash("Password must be at least eight characters in length")
        return is_valid