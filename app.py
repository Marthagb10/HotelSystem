from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '3306'
app.config['MYSQL_DB'] = 'hotel_db'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/clientes')
def clientes():

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM clientes")

    datos = cur.fetchall()

    return render_template(
        'clientes.html',
        clientes=datos
    )

@app.route('/add_cliente', methods=['POST'])
def add_cliente():

    if request.method == 'POST':

        nombre = request.form['nombre']
        cedula = request.form['cedula']
        telefono = request.form['telefono']
        direccion = request.form['direccion']

        cur = mysql.connection.cursor()

        cur.execute("""
            INSERT INTO clientes
            (nombre, cedula, telefono, direccion)
            VALUES (%s,%s,%s,%s)
        """, (nombre, cedula, telefono, direccion))

        mysql.connection.commit()

        return redirect('/clientes')

@app.route('/habitaciones')
def habitaciones():
    return "<h1>Modulo Habitaciones</h1>"

@app.route('/reservas')
def reservas():
    return "<h1>Modulo Reservas</h1>"

@app.route('/pagos')
def pagos():
    return "<h1>Modulo Pagos</h1>"

@app.route('/delete_cliente/<id>')
def delete_cliente(id):

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM clientes WHERE id_cliente=%s",
        (id,)
    )

    mysql.connection.commit()

    return redirect('/clientes')

if __name__ == '__main__':
    app.run(debug=True)