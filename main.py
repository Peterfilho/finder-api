from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

db_connect = create_engine('sqlite:///locale.db')
app = Flask(__name__)
api = Api(app)

app.config["DEBUG"] = True


class Users(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        cur = conn.cursor()
        all_users = cur.execute('SELECT * FROM users;').fetchall()

        return jsonify(all_users)

    def post(self):
        conn = db_connect.connect()
        print(request.json)
        Name = request.json['name']
        Department = request.json['department']
        Role = request.json['role']
        Ra = request.json['ra']
        query = conn.execute("insert into users values(null,'{0}','{1}','{2}','{3}')".format(Name,Department,Role,Ra))
        return {'status':'success'}


class Tracks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)


class Employees_Name(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from employees where EmployeeId =%d "  %int(employee_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)


api.add_resource(Users, '/users') # Route_1
api.add_resource(Tracks, '/tracks') # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3


if __name__ == '__main__':
     app.run()
