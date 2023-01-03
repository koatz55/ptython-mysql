import flask_app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.ninja import Ninjas
class Dojos:
    def __init__(self , db_data ):
        self.id = db_data['id']
        self.name = db_data['name']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.ninjas = []
    @classmethod
    def save( cls , data ):
        query = "INSERT INTO dojos ( name , created_at , updated_at ) VALUES (%(name)s,NOW(),NOW());"
        return connectToMySQL('dojos_and_ninjas_schema').query_db( query, data)

    @classmethod
    def get_one_with_ninjas(cls, data ):
        query = "SELECT * FROM dojos LEFT JOIN ninjas on dojos.id = ninjas.dojo_id WHERE dojos.id = %(id)s;"
        results = connectToMySQL('dojos_and_ninjas_schema').query_db(query,data)
        print(results)
        dojo = cls(results[0])
        for row in results:
            n = {
                'id': row['ninjas.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'age': row['age'],
                'dojo_id': row['dojo_id'],
                'created_at': row['ninjas.created_at'],
                'updated_at': row['ninjas.updated_at']
            }
            dojo.ninjas.append( Ninjas(n) )
        return dojo

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos;"
        dojos_from_db =  connectToMySQL('dojos_and_ninjas_schema').query_db(query)
        dojos =[]
        for dojo in dojos_from_db:
            dojos.append(cls(dojo))
        return dojos

    @classmethod
    def destroy_Dojo(cls,data):
        query = "DELETE FROM dojos WHERE id = %(id)s;"
        return connectToMySQL('dojos_and_ninjas_schema').query_db(query,data)

    @classmethod
    def update_dojo(cls,data):
        query = "UPDATE dojos SET name = %(name)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('dojos_and_ninjas_schema').query_db(query,data)
