import hashlib
import sqlite3
from flask import Flask, request

#crearemos una variable app para usar Flask

app = Flask(__name__)

#daremos nombre a nuestra base de datos

db_name = 'Ev3.db'

#crear un servicio web local
@app.route('/')
def index():
    return 'Bienvenido a mi base de datos SQL'

######################################### Texto Plano #########################################################
@app.route('/signup/v1', methods=['POST'])
def signup_v1():
    with sqlite3.connect('db_name') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS USER_PLAIN
                       (USERNAME TEXT PRIMARY KEY NOT NULL,
                        PASSWORD TEXT NOT NULL)''')
        try:
            conn.execute("INSERT INTO USER_PLAIN (USERNAME, PASSWORD) VALUES (?, ?)",
                         (request.form['username'], request.form['password']))
        except sqlite3.IntegrityError:
            return "Username has been registered"
        return "success registered"


def verify_plain(username, password):
    with sqlite3.connect('db_name') as conn:
        c = conn.cursor()
        query = "SELECT PASSWORD FROM USER_PLAIN WHERE USERNAME = ?"
        c.execute(query, (username,))
        resultado = c.fetchone()
        if not resultado:
            return False
        return resultado[0] == resultado

@app.route('/login/v1', methods=['POST'])
def login_v1():
    if verify_plain(request.form['username'], request.form['password']):
        return 'login success'
    else:
        return 'Invalid Username/Password'

######################################### hash contraseña #########################################################
@app.route('/signup/v2', methods=['POST'])
def signup_v2():
    username = request.form.get('username')
    password = request.form.get('password')

    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS USER_HASH (USERNAME TEXT PRIMARY KEY NOT NULL, HASH TEXT NOT NULL)")

    try:
        hash_value = hashlib.sha256(password.encode()).hexdigest()
        c.execute("INSERT INTO USER_HASH (USERNAME, HASH) VALUES (?, ?)", (username, hash_value))
        conn.commit()
    except sqlite3.IntegrityError:
        return "Username has been registered"
    
    conn.close()

    return "Registered success"

def verify_hash(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    query = "SELECT HASH FROM USER_HASH WHERE USERNAME = ?"
    c.execute(query, (username,))

    consulta = c.fetchone()
    
    conn.close()

    if consulta is None:
        return False
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return consulta[0] == hashed_password

@app.route('/login/v2', methods=['POST'])
def login_v2():
    username = request.form.get('username')
    password = request.form.get('password')

    if verify_hash(username, password):
        return 'login success'
    else:
        return 'Invalid username/password'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9500, ssl_context='adhoc')

