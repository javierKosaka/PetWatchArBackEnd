from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import os
import database as db

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "API de gestión de cuidadores"

# LOGIN ADMINISTRADOR
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    
    cursor = db.database.cursor()
    query = "SELECT * FROM ADMIN WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    cursor.close()
    
    if user:
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Invalid username or password"}), 401


# AGREGAR CUIDADOR
@app.route('/api/cuidador', methods=['POST'])
def add_cuidador():
    data = request.json
    NOMBRE = data['NOMBRE']
    APELLIDO = data['APELLIDO']
    CALIFICACION = data['CALIFICACION']
    REVIEWS = data['REVIEWS']
    MASCOTA = data['MASCOTA']

    if NOMBRE and APELLIDO and CALIFICACION and REVIEWS and MASCOTA:
        cursor = db.database.cursor()
        try:
            sql = "INSERT INTO petwatchar.CUIDADOR (NOMBRE, APELLIDO, CALIFICACION, REVIEWS, MASCOTA) VALUES (%s, %s, %s, %s, %s)"
            data = (NOMBRE, APELLIDO, CALIFICACION, REVIEWS, MASCOTA)
            cursor.execute(sql, data)
            db.database.commit()
            return jsonify({"message": "Cuidador agregado exitosamente"}), 201
        except Exception as e:
            return jsonify({"message": str(e)}), 500
        finally:
            cursor.close()
    return jsonify({"message": "Todos los campos son obligatorios"}), 400


# MOSTRAR CUIDADORES
@app.route('/api/cuidadores', methods=['GET'])
def get_cuidadores():
    cursor = db.database.cursor()
    try:
        cursor.execute("SELECT * FROM petwatchar.CUIDADOR")
        myresult = cursor.fetchall()
        columnNames = [column[0] for column in cursor.description]
        cuidadores = [dict(zip(columnNames, record)) for record in myresult]
        return jsonify(cuidadores)
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        cursor.close()

# BORRAR CUIDADORES
@app.route('/api/cuidador/<string:IDCUIDADOR>', methods=['DELETE'])
def delete_cuidador(IDCUIDADOR):
    cursor = db.database.cursor()
    try:
        sql = "DELETE FROM petwatchar.CUIDADOR WHERE IDCUIDADOR = %s"
        data = (IDCUIDADOR,)
        cursor.execute(sql, data)
        db.database.commit()
        return jsonify({"message": "Cuidador eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        cursor.close()

@app.route('/api/cuidador/<string:IDCUIDADOR>', methods=['PUT'])
def edit_cuidador(IDCUIDADOR):
    data = request.json
    NOMBRE = data['NOMBRE']
    APELLIDO = data['APELLIDO']
    CALIFICACION = data['CALIFICACION']
    REVIEWS = data['REVIEWS']
    MASCOTA = data['MASCOTA']

    if NOMBRE and APELLIDO and CALIFICACION and REVIEWS and MASCOTA:
        cursor = db.database.cursor()
        try:
            sql = "UPDATE petwatchar.CUIDADOR SET NOMBRE = %s, APELLIDO = %s, CALIFICACION = %s, REVIEWS = %s, MASCOTA = %s WHERE IDCUIDADOR = %s"
            data = (NOMBRE, APELLIDO, CALIFICACION, REVIEWS, MASCOTA, IDCUIDADOR)
            cursor.execute(sql, data)
            db.database.commit()
            return jsonify({"message": "Cuidador actualizado exitosamente"}), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 500
        finally:
            cursor.close()
    return jsonify({"message": "Todos los campos son obligatorios"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=4000)
