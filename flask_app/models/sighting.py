from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User

class Sighting:

    def __init__ (self, data):

        self.id = data['id']
        self.location = data['location']
        self.what_happened = data['what_happened']
        self.date_of = data['date_of']
        self.count = data['count']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.posting_user = None

    @classmethod
    def save(cls, data):
        if not cls.validate_sighting(data):
            return False

        query = 'INSERT INTO sightings (location, what_happened, date_of, count,user_id) VALUES (%(location)s, %(what_happened)s, %(date_of)s, %(count)s,%(user_id)s); '

        results = connectToMySQL('sasquatch_schema').query_db(query, data)

        return results

    @classmethod
    def validate_sighting(cls, data):
        is_valid = True
        if len(data['location']) < 3:
            flash('Invalid Location', 'sighting')
            is_valid = False
        if len( data['what_happened']) <= 0:
            flash('Invalid Response', 'sighting')
            is_valid = False
        if len( data['date_of']) <= 0:
            flash('Invalid Date.. this is important', 'sighting')
            is_valid = False
        if len( data['count']) <= 0:
            flash('You have to have seen atleast 1 squatch', 'sighting')
        return is_valid

    @classmethod
    def get_all(cls):
            query = 'SELECT * FROM sightings LEFT JOIN users ON sightings.user_id = users.id'

            results = connectToMySQL('sasquatch_schema').query_db(query)

            all_sightings = []

            for row in results:

                posting_user = User({
                    "id": row["users.id"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "email": row["email"],
                    "created_at": row["users.created_at"],
                    "updated_at": row["users.updated_at"],
                    "password": row["password"]
                })
                #  - make post instance with a user object
                sighting = cls(row)
                sighting.posting_user = posting_user
                # Add post to all_posts list
                all_sightings.append(sighting)

            return all_sightings

    @classmethod
    def delete_sighiting(cls, data):
        query = 'DELETE FROM sightings WHERE id = %(id)s'

        return connectToMySQL('sasquatch_schema').query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
            query = 'SELECT * FROM sightings LEFT JOIN users ON sightings.user_id = users.id WHERE sightings.id = %(id)s;'

            result = connectToMySQL('sasquatch_schema').query_db(query, data)

            result = result[0]
            this_sighting = cls(result)

            user_data ={
                    "id": result["user_id"],
                    "first_name": result["first_name"],
                    "last_name": result["last_name"],
                    "email": result["email"],
                    "created_at": result["users.created_at"],
                    "updated_at": result["users.updated_at"],
                    "password": result["password"]
                }
            this_sighting.posting_user = User(user_data)

            return this_sighting

    @classmethod
    def update(cls, data):
        if not cls.validate_sighting(data):
            return False

        query = 'UPDATE sightings SET location = %(location)s, what_happened = %(what_happened)s, date_of = %(date_of)s, count = %(count)s WHERE sightings.id = %(id)s'

        return connectToMySQL('sasquatch_schema').query_db(query, data)