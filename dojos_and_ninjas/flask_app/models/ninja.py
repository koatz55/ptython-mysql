from flask_app.config.mysqlconnection import connectToMySQL

class Ninjas:
    def __init__(self,data):
        self.id = data['id']
        self.first_name= data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.dojo_id = data['dojo_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO ninjas ( first_name , last_name , age , created_at , updated_at , dojo_id ) VALUES (%(first_name)s, %(last_name)s, %(age)s, NOW(),NOW(), %(dojo_id)s);"
        return connectToMySQL('dojos_and_ninjas_schema',).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM ninjas;"
        ninjas_from_db =  connectToMySQL('dojos_and_ninjas_schema').query_db(query)
        ninjas =[]
        for ninja in ninjas_from_db:
            ninjas.append(cls(ninja))
        return ninjas

    @classmethod
    def get_one(cls,data):
        query = "SELECT * from dojos_and_ninjas_schema.ninjas where ninjas.id = %(id)s;"
        ninja_from_db = connectToMySQL('dojos_and_ninjas_schema').query_db(query,data)

        return cls(ninja_from_db[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE ninjas SET first_name=%(first_name)s, last_name=%(last_name)s, age=%(age)s, dojo_id=%(dojo_id)s,updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('dojos_and_ninjas_schema').query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM ninjas WHERE id = %(id)s;"
        return connectToMySQL('dojos_and_ninjas_schema').query_db(query,data)

    @classmethod
    def get_dojo_id(cls,data):
        query = "SELECT dojo_id from ninjas WHERE id = %(id)s;"
        dojo_id = []
        ninjas_dojo_id = connectToMySQL("dojos_and_ninjas_schema").query_db(query,data)
        for id in ninjas_dojo_id:
            dojo_id.append(id)
        return dojo_id[0]
