from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "3306"
app.config["MYSQL_DB"] = "hotel_db"

mysql = MySQL(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/clientes")
def clientes():

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM clientes")

    datos = cur.fetchall()

    return render_template("clientes.html", clientes=datos)


@app.route("/add_cliente", methods=["POST"])
def add_cliente():

    if request.method == "POST":

        nombre = request.form["nombre"]
        cedula = request.form["cedula"]
        telefono = request.form["telefono"]
        direccion = request.form["direccion"]

        cur = mysql.connection.cursor()

        cur.execute(
            """
            INSERT INTO clientes
            (nombre, cedula, telefono, direccion)
            VALUES (%s,%s,%s,%s)
        """,
            (nombre, cedula, telefono, direccion),
        )

        mysql.connection.commit()

        return redirect("/clientes")

@app.route("/delete_cliente/<id>")
def delete_cliente(id):

    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM clientes WHERE id_cliente=%s", (id,))

    mysql.connection.commit()

    return redirect("/clientes")


@app.route("/edit_cliente/<id>")
def edit_cliente(id):

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM clientes WHERE id_cliente=%s", (id,))

    cliente = cur.fetchone()

    return render_template("edit_cliente.html", cliente=cliente)


@app.route("/update_cliente/<id>", methods=["POST"])
def update_cliente(id):

    nombre = request.form["nombre"]
    cedula = request.form["cedula"]
    telefono = request.form["telefono"]
    direccion = request.form["direccion"]

    cur = mysql.connection.cursor()

    cur.execute(
        """
        UPDATE clientes
        SET nombre=%s,
            cedula=%s,
            telefono=%s,
            direccion=%s
        WHERE id_cliente=%s
    """,
        (nombre, cedula, telefono, direccion, id),
    )

    mysql.connection.commit()

    return redirect("/clientes")

@app.route("/habitaciones")
def habitaciones():

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM habitaciones")

    habitaciones = cur.fetchall()

    return render_template("habitaciones.html", habitaciones=habitaciones)


@app.route("/add_habitacion", methods=["POST"])
def add_habitacion():

    numero = request.form["numero"]
    tipo = request.form["tipo"]
    precio = request.form["precio"]
    estado = request.form["estado"]

    cur = mysql.connection.cursor()

    cur.execute(
        """
        INSERT INTO habitaciones
        (numero, tipo, precio, estado)
        VALUES (%s,%s,%s,%s)
    """,
        (numero, tipo, precio, estado),
    )

    mysql.connection.commit()

    return redirect("/habitaciones")

@app.route('/delete_habitacion/<id>')
def delete_habitacion(id):

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM habitaciones WHERE id_habitacion=%s",
        (id,)
    )

    mysql.connection.commit()

    return redirect('/habitaciones')

@app.route('/edit_habitacion/<id>')
def edit_habitacion(id):

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM habitaciones WHERE id_habitacion=%s",
        (id,)
    )

    habitacion = cur.fetchone()

    return render_template(
        'edit_habitacion.html',
        habitacion=habitacion
    )

@app.route('/update_habitacion/<id>', methods=['POST'])
def update_habitacion(id):

    numero = request.form['numero']
    tipo = request.form['tipo']
    precio = request.form['precio']
    estado = request.form['estado']

    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE habitaciones
        SET numero=%s,
            tipo=%s,
            precio=%s,
            estado=%s
        WHERE id_habitacion=%s
    """, (numero, tipo, precio, estado, id))

    mysql.connection.commit()

    return redirect('/habitaciones')

@app.route('/reservas')
def reservas():

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            r.id_reserva,
            r.fecha_ingreso,
            r.fecha_salida,
            c.nombre,
            h.numero
        FROM reservas r
        INNER JOIN clientes c
            ON r.id_cliente = c.id_cliente
        INNER JOIN habitaciones h
            ON r.id_habitacion = h.id_habitacion
    """)

    reservas = cur.fetchall()

    cur.execute("SELECT * FROM clientes")
    clientes = cur.fetchall()

    cur.execute("SELECT * FROM habitaciones")
    habitaciones = cur.fetchall()

    return render_template(
        'reservas.html',
        reservas=reservas,
        clientes=clientes,
        habitaciones=habitaciones
    )

@app.route('/add_reserva', methods=['POST'])
def add_reserva():

    fecha_ingreso = request.form['fecha_ingreso']
    fecha_salida = request.form['fecha_salida']
    id_cliente = request.form['id_cliente']
    id_habitacion = request.form['id_habitacion']

    cur = mysql.connection.cursor()

    cur.execute("""
        INSERT INTO reservas
        (fecha_ingreso, fecha_salida, id_cliente, id_habitacion)
        VALUES (%s,%s,%s,%s)
    """, (
        fecha_ingreso,
        fecha_salida,
        id_cliente,
        id_habitacion
    ))

    mysql.connection.commit()

    return redirect('/reservas')

@app.route('/delete_reserva/<id>')
def delete_reserva(id):

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM reservas WHERE id_reserva=%s",
        (id,)
    )

    mysql.connection.commit()

    return redirect('/reservas')

@app.route('/edit_reserva/<id>')
def edit_reserva(id):

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM reservas WHERE id_reserva=%s",
        (id,)
    )

    reserva = cur.fetchone()

    cur.execute("SELECT * FROM clientes")
    clientes = cur.fetchall()

    cur.execute("SELECT * FROM habitaciones")
    habitaciones = cur.fetchall()

    return render_template(
        'edit_reserva.html',
        reserva=reserva,
        clientes=clientes,
        habitaciones=habitaciones
    )

@app.route('/update_reserva/<id>', methods=['POST'])
def update_reserva(id):

    fecha_ingreso = request.form['fecha_ingreso']
    fecha_salida = request.form['fecha_salida']
    id_cliente = request.form['id_cliente']
    id_habitacion = request.form['id_habitacion']

    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE reservas
        SET fecha_ingreso=%s,
            fecha_salida=%s,
            id_cliente=%s,
            id_habitacion=%s
        WHERE id_reserva=%s
    """, (
        fecha_ingreso,
        fecha_salida,
        id_cliente,
        id_habitacion,
        id
    ))

    mysql.connection.commit()

    return redirect('/reservas')

@app.route("/pagos")
def pagos():
    return "<h1>Modulo Pagos</h1>"


if __name__ == '__main__':
    app.run(debug=True)
