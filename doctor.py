from flask import Flask, Blueprint, render_template,request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

doctores = Flask(__name__)
# conexion con la base de datos
doctores.config['MYSQL_HOST'] = 'localhost'
doctores.config['MYSQL_USER'] = 'root'
doctores.config['MYSQL_PASSWORD'] = ''
doctores.config['MYSQL_DB'] = 'bd_cento_medico'

#preparar la conexion con la base de datos
mysql = MySQL(doctores)

# setting
doctores.secret_key = 'nashe2'

second = Blueprint('second', __name__, )


############ solo retornan VISTAS ############## 


@second.route('/doctor')
def doctores():
     # verificar la sesion del usuario
    if 'rfc' in session:
        # obtener el nombre y pasarlo al template
        rfc = session['rfc']
        # sql para obtener el nombre del doctor donde el RFC = nombre
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT Nombre FROM tb_doctores WHERE RFC = %s', (rfc,))
        nombre = cursor.fetchone()
        nombre = nombre[0]
        # consultar la base de datos
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM tb_doctores')
        data = cur.fetchall()
        return render_template('doctor.html', doctores=data, nombre=nombre, rfc=rfc)

@second.route('/doctores/verPacientes')
def verMisPacientes():
      if 'rfc' in session:
        # obtener el nombre y pasarlo al template
        rfc = session['rfc']
        # obtener el id del doctor de la sesion
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id_doctor FROM tb_doctores WHERE RFC = %s', (rfc,))
        id_doctor = cursor.fetchone()
        # sql para obtener el nombre del doctor donde el RFC = nombre
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT Nombre FROM tb_doctores WHERE RFC = %s', (rfc,))
        nombre = cursor.fetchone()
        nombre = nombre[0]
        # consultar la base de datos
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM tb_expedientes WHERE id_doctor = %s', (id_doctor[0],))
        data = cur.fetchall()
        return render_template('doctorNormal/verPacientes.html', expedientes=data, nombre=nombre, rfc=rfc)

@second.route('/doctores/pacientes')
def doctorPacientes(): 
     # verificar la sesion del usuario
    if 'rfc' in session:
        # obtener el nombre y pasarlo al template
        rfc = session['rfc']
        # sql para obtener el nombre del doctor donde el RFC = nombre
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT Nombre FROM tb_doctores WHERE RFC = %s', (rfc,))
        nombre = cursor.fetchone()
        nombre = nombre[0]
        # consultar la base de datos
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM tb_doctores')
        data = cur.fetchall()
        return render_template('doctorNormal/pacientes.html', doctores=data, nombre=nombre, rfc=rfc)

@second.route('/doctores/exploracion_diagnostico')
def exploracionDiagnostico():
    if 'rfc' in session:
        # obtener el nombre y pasarlo al template
        rfc = session['rfc']
        # obtener el id del doctor de la sesion
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT Cedula FROM tb_doctores WHERE RFC = %s', (rfc,))
        cedula = cursor.fetchone()
        # sql para obtener el nombre del doctor donde el RFC = nombre
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT Nombre FROM tb_doctores WHERE RFC = %s', (rfc,))
        nombre = cursor.fetchone()
        nombre = nombre[0]
        # seleccionar id del doctor
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id_doctor FROM tb_doctores WHERE RFC = %s', (rfc,))
        id_doctor = cursor.fetchone()

        # consultar todos los pacientes del doctor en session y mandarlos al template
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM tb_expedientes WHERE id_doctor = %s', (id_doctor[0],))
        data = cur.fetchall()

        


        return render_template('doctorNormal/exploracionDiagnostico.html',  nombre=nombre, rfc=rfc, cedula = cedula[0], pacientes = data)

@second.route('/consultarCitas')
def consultarCitas():
   if 'rfc' in session:
        # obtener el nombre y pasarlo al template
        rfc = session['rfc']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT Nombre FROM tb_doctores WHERE RFC = %s', (rfc,))
        nombre = cursor.fetchone()
        nombre = nombre[0]
         # obtener el id_doctor  en sesion
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id_doctor FROM tb_doctores WHERE RFC = %s', (session['rfc'],))
        id_doctor = cursor.fetchone()

        # consultar las citas donde el id_expediente = id_expediente OR la fecha_cita = Fecha de la tb_cita
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM tb_citas WHERE id_doctor = %s', (id_doctor[0],))
        data = cur.fetchall()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM tb_expedientes')
        data2 = cur.fetchall()

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT Cedula FROM tb_doctores WHERE RFC = %s', (rfc,))
        cedula = cursor.fetchone()
        cedula = cedula[0]

        return render_template('doctorNormal/verCitas.html',  nombre=nombre, rfc=rfc, citas = data, pacientes = data2, cedula = cedula)


############ FIN solo retornan VISTAS ############## 

@second.route('/doctor/registrar_paciente', methods=['GET', 'POST'])
def doctorRegistrarPaciente():
    if request.method == 'POST':
        # obtener los datos del forms
        nombre = request.form['nombre']
        fecha_nacimiento = request.form['fecha']
        enfermedades = request.form['enfermedades']
        alergias = request.form['alergias']
        antecedentes = request.form['antecedentes']

        # buscar el id del doctor que inicio sesion
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id_doctor FROM tb_doctores WHERE RFC = %s', [session['rfc']])
        # guardar el id del doctor en una variable
        id_doctor = cursor.fetchone()
        
        # crear una consulta para verificar los datos
        cursor = mysql.connection.cursor()
        # insertar los datos en la base de datos tb_expedientes
        cursor.execute('INSERT INTO tb_expedientes (id_doctor, Nombre, Fecha_Nacimiento, Enfermedades, Alergias, Antecedentes) VALUES (%s, %s, %s, %s, %s, %s)', (id_doctor[0],nombre, fecha_nacimiento, enfermedades, alergias, antecedentes))
        # guardar los cambios
        mysql.connection.commit()
        flash('El paciente ha sido registrado con exito!')
        return redirect(url_for('second.doctorPacientes'))

@second.route('/editar_paciente', methods=['GET', 'POST'])
def editar_paciente():
    #obtener los valores del formulario
    nombre_paciente = request.form['nombre_nuevo']
    fecha_nacimiento_paciente = request.form['fecha_nacimiento_nuevo']
    enfermedades = request.form['enfermedades_nuevo']
    alergias = request.form['alergias_nuevo']
    antecedentes = request.form['antecedentes_nuevo']
    id_paciente = request.form['id_paciente']
    # obtener el id del doctor en sesion
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id_doctor FROM tb_doctores WHERE RFC = %s', [session['rfc']])
    # guardar el id del doctor en una variable
    id_doctor = cursor.fetchone()
    # crear una consulta para actualizar los datos
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE tb_expedientes SET id_doctor = %s, Nombre = %s, Fecha_Nacimiento = %s, Enfermedades = %s, Alergias = %s, Antecedentes = %s WHERE id_expediente = %s', (id_doctor[0], nombre_paciente, fecha_nacimiento_paciente, enfermedades, alergias, antecedentes, id_paciente))

    # guardar los cambios
    mysql.connection.commit()
    flash('El paciente ha sido editado con exito!')
    return redirect(url_for('second.verMisPacientes'))


@second.route('/doctor/guardar_cita', methods=['GET', 'POST'])
def guardarCita():
    if request.method == 'POST':
        
        nombre_paciente = request.form['listaPacientes']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id_expediente FROM tb_expedientes WHERE Nombre = %s', [nombre_paciente])
        # guardar el id del paciente en una variable
        id_expediente = cursor.fetchone()

        # obtener el id del doctor en sesion
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id_doctor FROM tb_doctores WHERE RFC = %s', [session['rfc']])
        # guardar el id del doctor en una variable
        id_doctor = cursor.fetchone()
        
        # obtener los datos del formulario
        fecha = request.form['fecha_hora']
        peso = request.form['peso']
        altura = request.form['altura']
        temperatura = request.form['temperatura']
        latidos = request.form['latidos']
        saturacion = request.form['saturacion']
        glucosa = request.form['glucosa']
        edad = request.form['edad']
        sintomas = request.form['sintomas']
        tratamiento = request.form['medicamentos']
        indicaciones = request.form['indicaciones']

        # verificar si el nombre del paciente existe en la base de datos y esta relacionado al doctor en sesion
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id_expediente FROM tb_expedientes WHERE Nombre = %s AND id_doctor = %s', (nombre_paciente, id_doctor[0]))

        # si existe el paciente y esta relacionado al doctor en sesion seguir con el proceso de guardar la cita
        if cursor.fetchone():
            # guardar los datos en la tabla tb_citas
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO tb_citas (id_expediente, id_doctor, Fecha, Peso, Altura, Temperatura, Latidos, Saturacion_oxigeno, Glucosa, Edad, Sintomas, Tratamiento, Indicaciones) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (id_expediente[0], id_doctor[0], fecha, peso, altura, temperatura, latidos, saturacion, glucosa, edad, sintomas, tratamiento, indicaciones))

            # guardar los cambios
            mysql.connection.commit()
            flash('Datos guardados con exito!')
            return redirect(url_for('second.exploracionDiagnostico'))
        else:
            flash('El paciente no existe o no esta relacionado al doctor en sesion!')
            return redirect(url_for('second.exploracionDiagnostico'))
    else:
        print('no se pudo guardar')
        return redirect(url_for('second.exploracionDiagnostico'))   

@second.route('/filtrar_cita_por_nombre', methods=['POST'])
def filtrarCitaPorNombre():
    if request.method == 'POST':
        # obtener los datos de la forma
        nombre = request.form['nombre_paciente']

        # obtener el id_expediente del paciente
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id_expediente FROM tb_expedientes WHERE Nombre = %s', (nombre,))
        id_expediente = cursor.fetchone()

        # si no existe el expediente mandar un mensaje
        if id_expediente is None:
            flash('No existe el paciente')
            return redirect(url_for('second.consultarCitas'))
        else: 
            # obtener el id_doctor en sesion
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT id_doctor FROM tb_doctores WHERE RFC = %s', (session['rfc'],))
            id_doctor = cursor.fetchone()
            rfc = session['rfc']
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT Nombre FROM tb_doctores WHERE RFC = %s', (rfc,))
            nombre = cursor.fetchone()
            nombreDoctor = nombre[0]

            # consultar las citas donde el id_expediente = id_expediente y id_doctor = id_doctor en la tabla tb_citas
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM tb_citas WHERE id_expediente = %s AND id_doctor = %s', (id_expediente[0], id_doctor[0]))
            data = cur.fetchall()
            # si no hay datos mandar un mensaje
            if len(data) == 0:
                flash('Existe el paciente, pero esta registrado con otro doctor, verifique la informacion') 
                return render_template('doctorNormal/verCitas.html',  nombre=nombreDoctor, rfc=rfc, citas = data)
            else:
                flash('Citas encontradas')
                return render_template('doctorNormal/verCitas.html',  nombre=nombreDoctor, rfc=rfc, citas = data)
    else:
        flash('No se pudo filtrar la cita')
        return redirect(url_for('second.consultarCitas'))


@second.route('/filtrar_cita_por_fecha', methods=['POST'])
def filtrarCitaPorFecha():
    if request.method == 'POST':
        # obtener los datos de la forma
        fechaCita = request.form['fecha_cita']

        
        # obtener el id_doctor en sesion
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id_doctor FROM tb_doctores WHERE RFC = %s', (session['rfc'],))
        id_doctor = cursor.fetchone()

        rfc = session['rfc']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT Nombre FROM tb_doctores WHERE RFC = %s', (rfc,))
        nombreDr = cursor.fetchone()
        nombreDoctor = nombreDr[0]

        # consultar las citas donde la Fecha = fecha_cita y id_doctor = id_doctor en la tabla tb_citas
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM tb_citas WHERE Fecha = %s AND id_doctor = %s', (fechaCita, id_doctor[0]))
        data = cur.fetchall()
        # si no hay datos mandar un mensaje
        if len(data) == 0:
            flash('No hay citas para la fecha seleccionada')
            return render_template('doctorNormal/verCitas.html',  nombre=nombreDoctor, rfc=rfc, citas = data)
        else:
            flash('Citas encontradas')
            return render_template('doctorNormal/verCitas.html',  nombre=nombreDoctor, rfc=rfc, citas = data)