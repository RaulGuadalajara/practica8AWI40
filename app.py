from flask import Flask, render_template, request, jsonify, make_response
import mysql.connector
from flask_cors import CORS

# Configuración de la conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host="82.197.82.90",
        database="u861594054_p8_awi40_db5",
        user="u861594054_yosoyRaul",
        password="1w+Rq4x32P*Q"
    )

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/app")
def app2():
    return "<h5>Práctica 8 - Raul Omar Guadalajara Sanchez</h5>"

@app.route("/decoraciones")
def decoraciones():
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM decoraciones LIMIT 10 OFFSET 0")
    registros = cursor.fetchall()
    
    con.close()
    return render_template("Decoraciones.html", decoraciones=registros)

@app.route("/decoraciones/buscar", methods=["GET"])
def buscarDecoraciones():
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    
    busqueda = f"%{request.args.get('busqueda', '')}%"
    
    sql = "SELECT * FROM decoraciones WHERE nombreMaterial LIKE %s ORDER BY idDecoracion DESC LIMIT 10"
    cursor.execute(sql, (busqueda,))
    
    registros = cursor.fetchall()
    
    con.close()
    return make_response(jsonify(registros))

@app.route("/decoracion", methods=["POST"])
def guardarDecoracion():
    con = get_db_connection()
    cursor = con.cursor()
    
    id = request.form.get("idDecoracion")
    material = request.form.get("nombreMaterial")
    
    if id:
        sql = "UPDATE decoraciones SET nombreMaterial = %s WHERE idDecoracion = %s"
        val = (material, id)
    else:
        sql = "INSERT INTO decoraciones (nombreMaterial) VALUES (%s)"
        val = (material,)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    return make_response(jsonify({"success": True}))

@app.route("/decoraciones/<int:id>")
def editarDecoracion(id):
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    
    cursor.execute("SELECT idDecoracion, nombreMaterial FROM decoraciones WHERE idDecoracion = %s", (id,))
    registro = cursor.fetchone()
    
    con.close()
    return make_response(jsonify(registro))

@app.route("/decoracion/eliminar", methods=["POST"])
def eliminarDecoracion():
    con = get_db_connection()
    cursor = con.cursor()
    
    id = request.form.get("idDecoracion")
    
    cursor.execute("DELETE FROM decoraciones WHERE idDecoracion = %s", (id,))
    con.commit()
    
    con.close()
    return make_response(jsonify({"success": True}))
