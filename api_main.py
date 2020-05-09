import flask
from flask import request, jsonify
import numpy as np
import sqlite3
from json import dumps
import requests
import json
import localize
import os

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Were i am</h1>
<p>A prototype API to localize users using ieee 802.11.</p>

<p> Developed by: Peterson Medeiros</p>'''
#SQL COMMANDS - TEST ROTE
@app.route('/api/test', methods=['GET'])
def test():
    conn = sqlite3.connect('locale.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
#    all_users = cur.execute('SELECT *, users.* from positions join users using(user_id) WHERE user_id=1;').fetchall()
#    all_users = cur.execute('SELECT *, users.* from positions join users using(user_id);').fetchall()
    all_users = cur.execute('SELECT * from positions ORDER BY position_id DESC;').fetchall()
    return jsonify({'TEST Result': all_users})
    conn.close()

#TODO INSERT A IMAGE OFF MAP WERE IS
@app.route('/api/v1/resources/map', methods=['GET'])
def map():
    url = "https://drive.google.com/open?id=1Nf7s7I3iWIKLeMhF5iRjG9u7dQpOLtD8"
    result = requests.get(url).json()
    return (result)

@app.route('/api/v1/resources/users/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('locale.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_users = cur.execute('SELECT * FROM users ORDER BY user_id DESC;').fetchall()

    return jsonify({'users': all_users})
    conn.close()

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/api/v1/resources/users', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    department = query_parameters.get('department')
    role = query_parameters.get('role')

    query = "SELECT * FROM users WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if department:
        query += ' department=? AND'
        to_filter.append(department)
    if role:
        query += ' role=? AND'
        to_filter.append(role)
    if not (id or department or role):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('locale.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)
    conn.close()

@app.route('/api/v1/resources/users', methods=['POST'])
def post():
    conn = sqlite3.connect('locale.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    user = request.get_json()
    print("o que chega?")
    print(user)

    #for user in users:
    user_id = user['ra']
    name = user['name']
    department = user['department']
    role = user['role']

    print("insert into users values('{}', '{}','{}','{}')".format(user_id, name, department, role))
    cur.execute("insert into users values('{}','{}','{}','{}')".format(user_id, name, department, role))
    conn.commit()
    return {'Success': user}
    conn.close()

@app.route('/api/v1/resources/positions/all', methods=['GET'])
def locales_all():
    conn = sqlite3.connect('locale.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_users = cur.execute('SELECT * FROM positions ORDER BY position_id DESC;').fetchall()

    return jsonify({'users': all_users})
    conn.close()

@app.route('/api/v1/resources/positions', methods=['GET'])
def locales():
    query_parameters = request.args
#PARAMETERS ON URL
    id = query_parameters.get('ra')
    name = query_parameters.get('name')
    date = query_parameters.get('date')
    locale = query_parameters.get('locale')
    role = query_parameters.get('role')

    query = "SELECT *, users.* FROM positions join users using (user_id) WHERE"
    to_filter = []

    if id:
        query += ' user_id=? AND'
        to_filter.append(id)
    if date:
        query += ' date=? AND'
        to_filter.append(date)
    if locale:
        query += ' locale=? AND'
        to_filter.append(locale)
    if role:
        query += ' users.role=? AND'
        to_filter.append(role)
    if name:
        query += ' users.name=? AND'
        to_filter.append(name)

    if not (id or date or locale or role or name):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('locale.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)
    conn.close()

@app.route('/api/v1/resources/positions/last', methods=['GET'])
def last_locales():
    query_parameters = request.args
#PARAMETERS ON URL
    id = query_parameters.get('id')
    name = query_parameters.get('name')
    date = query_parameters.get('date')
    locale = query_parameters.get('locale')

    query = "SELECT *, users.* FROM positions join users using MAX(user_id) WHERE"
    to_filter = []

    if id:
        query += ' user_id=? AND'
        to_filter.append(id)
    if date:
        query += ' date=? AND'
        to_filter.append(date)
    if locale:
        query += ' locale=? AND'
        to_filter.append(locale)
    if name:
        query += ' users.name=? AND'
        to_filter.append(name)

    if not (id or date or locale or name):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('locale.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)
    conn.close()

@app.route('/api/v1/resources/positions', methods=['POST'])
def positions_post():
    conn = sqlite3.connect('locale.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    users = request.get_json()
    for user in users:
        user_id = user['user_id']
        search = user['search']
        result = user['result']
        locale = user['locale']
        date = user['date']
        cur.execute("insert into positions values(NULL, '{}','{}','{}','{}','{}')".format(user_id, search, result, locale, date))
        conn.commit()
    return {'status':'success'}
    conn.close()

@app.route('/api/v1/resources/positions/app', methods=['POST'])
def positions_post_app():
    conn = sqlite3.connect('locale.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
#    data = json.loads(request.get_json())
    data = request.get_json()
    print("Content in POST")
    print(data)
    user_id = data['user_id']
    find = data['search']
    date = data['date']
#    print("valor que chega!")
#    print(find)
    valores = find.split(",")
#        print("lista de inteiros")
#        print(valores)
#        aux = localize.localize(-100,-70,-68,-55,-53,-55)
#        valores[0],valores[1],valores[2],valores[3],valores[4],valores[5]

    aux = localize.localize(valores[0],valores[1],valores[2],valores[3],valores[4],valores[5])

    print("Chegando apos rodar no localize")
    print(aux)

    if aux == None:
        print("Não encontrado ou fora de alcance")
        locale = "fora de alcance"
        result = "-100,-100,-100,-100,-100,-100"

    locale = aux['locale']
    result = aux['result']
    #convert a list of integers to string
    result = ','.join([str(elem) for elem in result])
    print("insert into positions values(NULL, '{}','{}', '{}', '{}', '{}')".format(user_id, find, result, locale, date))

    cur.execute("INSERT INTO positions VALUES (NULL, '{}', '{}', '{}', '{}', '{}')".format(user_id, find, result, locale, date))
    conn.commit()
    return {'Status': 'Success'}
    conn.close()

#app.run()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
