from crypt import methods
from dataclasses import dataclass
from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
# to start the project I first built the menu. Then started to create the sql python functions that interacted with the database.
# After this I started to add the sub menu, depending on the use, like the update function should show the cars so the user could
# select the right car to update
#this the the main conection function

#I started with the connection to the db
def conn_connection(hostname,connp, username, passwd, dbname):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = hostname,
            port = connp,
            user = username,
            password = passwd,
            database = dbname
        )
        print("Connection Success")
    except Error as e:
        print(f'The error {e}')
    return connection
conn = conn_connection()
curr = conn.cursor(dictionary = True)

# then initalized flask
app = Flask(__name__)
#this is the log function the is used by the backend
def animal_log(action, animal= 'animal'):
    sql = 'SELECT COUNT(id) from zoo'
    curr.execute(sql)
    id = curr.fetchmany(size=1)[0]['COUNT(id)']
    sql = "insert into logs values (null, now(), %s, %s)"
    curr.execute(sql, (id,'{} new {} to zoo'.format(action, animal),))
    curr.execute('commit;')
    return
#then I crated each function to interact with the db 
def add_animal(animal, gender, subype, age, color):
    sql = 'insert into zoo values (null, %s, %s, %s, %s, %s);'
    data = (animal, gender, subype, age, color)
    curr.execute(sql, data)
    id = curr.lastrowid
    curr.execute('commit;')
    #after the first insert i create a log function to log all the insert, updates and deletes
    animal_log('added',animal)
#this function gets the animals 
def get_animals():
    sql = 'select * from zoo;'
    curr.execute(sql)
    qurey = curr.fetchall()
 
    return qurey
#this function updates an animal based off the id
def animal_put(animal, gender, subype, age, color, id):
    sql = 'update zoo set animal=%s, gender=%s, subtype=%s, age=%s, color=%s where id=%s'
    data = (animal, gender, subype, age, color, id)
    curr.execute(sql, data)
    curr.execute('commit;')
    animal_log('updated', animal)
    return
# this function delete the animal from the id
def delete(id):
    sql = 'DELETE FROM zoo WHERE id=%s;'
    curr.execute(sql, (id,))
    curr.execute('commit;')
    animal_log('delete')
    return
#then created and empty animal get post put and delete endpoints with passes 
@app.route('/api/animal', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def zoo():
    page = request.form
    animals = get_animals()
    # i started to create each get post put and delete in that order
    if request.method == 'GET':
        return jsonify([animal for animal in animals])
    elif request.method == 'POST':
        animal = page['animal']
        gender = page['gender']
        sub = page['subtype']
        age = page['age']
        color = page['color']
        add_animal(animal, gender, sub, age, color)
        return 'Success'
    elif request.method == 'PUT':
        animal = page['animal']
        gender = page['gender']
        sub = page['subtype']
        age = page['age']
        color = page['color']
        id = page['id']
        animal_put(animal, gender, sub, age, color, id)
        return 'Success'
    elif request.method == 'DELETE':
        id = page['id']
        delete(id)
        return 'Success'
def get_logs():
    sql = 'select * from logs'
    curr.execute(sql)
    return curr.fetchall()
def delete_logs():
    sql = 'delete from logs'
    curr.execute(sql)
    return

#once i completed the animal endpoint i create the get log
@app.route('/api/logs', methods=['GET'])
def all_logs():
    #once i had a base to get all the logs I created the delete all logs
    if request.args.get('reset'):
        delete_logs()
        return 'Seccess'
    else:
        logs = get_logs()
        return jsonify([log for log in logs])

