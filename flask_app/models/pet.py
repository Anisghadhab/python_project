from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

# create a regular expression object that we'll use later


class Pet:
    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.name = data["name"]
        self.age = data["age"]
        self.breed = data["breed"]
        self.friendly_pets = data["friendly_pets"]
        self.friendly_children = data["friendly_children"]
        self.feeding_time = data["feeding_time"]
        self.special_requirement = data["special_requirement"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def create_pet(cls, data):
        query = """
        
        INSERT INTO pets (user_id, name, age, breed, friendly_pets, friendly_children, feeding_time, special_requirement)
        VALUES (%(user_id)s,%(name)s,%(age)s,%(breed)s,%(friendly_pets)s,%(friendly_children)s,%(feeding_time)s,%(special_requirement)s)
        
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete_pet(cls, data):
        query = """
        DELETE FROM pets
        WHERE id = %(id)s;

        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def update_pets(cls,data):
        query="""
        UPDATE pets SET
        name=%(name)s,age=%(age)s,is_dog=%(is_dog)s,breed=%(breed)s,
        friendly_pets=%(friendly_pets)s,friendly_children=%(friendly_children)s,
        feeding_times=%(feeding_times)s,special_requirement=%(special_requirement)s
        WHERE id = %(id)s ;
        """
        return connectToMySQL(DATABASE).query_db(query,data)
