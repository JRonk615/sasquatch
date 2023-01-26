from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        


    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL('sasquatch_schema').query_db(query, user)
        if len(results) >= 1:
            flash("email is already taken.", "register")
            is_valid = False
        if len(user['first_name']) <= 0:
            flash("Name must be at least 3 characters.", "register")
            is_valid = False
        if len(user['last_name']) <= 0:
            flash("Name must be at least 3 characters.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("invalid email", "register")
            is_valid = False
        if len(user['password']) <= 6:
            flash("invalid password", "register")
            is_valid = False
        if user['password'] != user['confirm']:
            flash('passwords dont match', "register")
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'

        results = connectToMySQL('sasquatch_schema').query_db(query, data)

        if len(results) < 1:
            return False

        return cls(results[0])
    
    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'

        results = connectToMySQL('sasquatch_schema').query_db(query, data)

        return cls(results[0])


    @classmethod
    def get_all(cls):

        query = 'SELECT * FROM users;'

        user_from_db = connectToMySQL('sasquatch_schema').query_db(query)

        users = []

        for user in user_from_db:
            users.append( cls(user))

        return users
    
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW() );'

        return connectToMySQL('sasquatch_schema').query_db(query, data)