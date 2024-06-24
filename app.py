from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'templates')


app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM petwatchar.CUIDADOR")
    myresult = cursor.fetchall()
    # convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('crud.html', data=insertObject)

# agregar registros del cuidador en base
@app.route('/cuidador', methods=['POST'])
def addCuidador():
    NOMBRE = request.form['NOMBRE']
    APELLIDO = request.form['APELLIDO']
    CALIFICACION = request.form['CALIFICACION']
    REVIEWS = request.form['REVIEWS']
    MASCOTA = request.form['MASCOTA']

    if NOMBRE and APELLIDO and CALIFICACION and REVIEWS and MASCOTA:
        cursor = db.database.cursor()
        sql = "INSERT INTO petwatchar.CUIDADOR (NOMBRE, APELLIDO, CALIFICACION, REVIEWS, MASCOTA) VALUES (%s, %s, %s, %s, %s)"
        data = (NOMBRE, APELLIDO, CALIFICACION, REVIEWS, MASCOTA)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))
        
# eliminar registros de la base de datos
@app.route('/delete/<string:IDCUIDADOR>')
def delete(IDCUIDADOR):
    cursor = db.database.cursor()
    sql = "DELETE FROM petwatchar.CUIDADOR WHERE IDCUIDADOR = %s"
    data = (IDCUIDADOR,) #MODIFICADO
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))
    

# modificar registros de la base de datos
@app.route('/edit/<string:IDCUIDADOR>', methods=['POST'])
def edit(IDCUIDADOR):
    NOMBRE = request.form['NOMBRE']
    APELLIDO = request.form['APELLIDO']
    CALIFICACION = request.form['CALIFICACION']
    REVIEWS = request.form['REVIEWS']
    MASCOTA = request.form['MASCOTA']

    if NOMBRE and APELLIDO and CALIFICACION and REVIEWS and MASCOTA:
        cursor = db.database.cursor()
        sql = "UPDATE petwatchar.CUIDADOR SET NOMBRE = %s, APELLIDO = %s, CALIFICACION = %s, REVIEWS = %s, MASCOTA = %s WHERE IDCUIDADOR = %s"
        data = (NOMBRE, APELLIDO, CALIFICACION, REVIEWS, MASCOTA, IDCUIDADOR)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))
    



if __name__ == '__main__':
    app.run(debug=True, port=4000)