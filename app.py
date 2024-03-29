from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from passlib.context import CryptContext
from doctor import second


app = Flask(__name__)
app.register_blueprint(second)

# conexion con la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bd_cento_medico'

# setting
app.secret_key = 'nashe'

#preparar la conexion con la base de datos
mysql = MySQL(app)

# para hashear las contaseñas
contexto = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)

# crear una ruta para la raiz de la aplicacion
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admins')
def admins():
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
        return render_template('admin/admins.html', doctores=data, nombre=nombre, rfc=rfc)

@app.route('/pacientes')
def pacientes():
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
        return render_template('pacientes.html', doctores=data, nombre=nombre, rfc=rfc)

@app.route('/ver_pacientes')
def verPacientes():
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
        return render_template('verPacientes.html', expedientes=data, nombre=nombre, rfc=rfc)


@app.route('/exploracion_diagnostico')
def exploracion_diagnostico():
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

        return render_template('exploracionDiagnostico.html',  nombre=nombre, rfc=rfc, cedula = cedula[0], pacientes = data)

@app.route('/consultar_citas')
def consultar_citas():
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
        return render_template('verCitas.html',  nombre=nombre, rfc=rfc, citas = data)


@app.route('/filtrar_cita_por_nombre', methods=['POST'])
def filtrar_cita_por_nombre():
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
            return redirect(url_for('consultar_citas'))
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
                return render_template('verCitas.html',  nombre=nombreDoctor, rfc=rfc, citas = data)
            else:
                flash('Citas encontradas')
                return render_template('verCitas.html',  nombre=nombreDoctor, rfc=rfc, citas = data)
    else:
        flash('No se pudo filtrar la cita')
        return redirect(url_for('consultar_citas'))


@app.route('/filtrar_cita_por_fecha', methods=['POST'])
def filtrar_cita_por_fecha():
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
        return render_template('citasFiltradasFecha.html',  nombre=nombreDoctor, rfc=rfc, citas = data)

#Un "middleware" que se ejecuta antes de responder a cualquier ruta. Aquí verificamos si el usuario ha iniciado sesión
@app.before_request
def verificarSesion():
     ruta = request.path
     # Si no ha iniciado sesión y quiere ir a algo no relacionado al login, lo redireccionamos al login
     if not 'rfc' in session and ruta != "/login" and ruta != "/" and ruta != "/index" and not ruta.startswith("/static"):
        flash("Inicia sesión para continuar")
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # obtener los datos de la forma
        user = request.form['rfc']
        password = request.form['pass']
        admin = 'admin'
        doctor = 'doctor'

        # crear una consulta para verificar los datos
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM tb_doctores WHERE RFC = %s', [user])
        
        # ejeutar la consulta fetchall() para obtener todos los registros
        data = cursor.fetchall()

        # obtener el rol del usuario
        cursor.execute('SELECT Rol FROM tb_doctores WHERE RFC = %s', [user])
        rol = cursor.fetchall()

        # verificar si el usuario existe, si existe verificar su rol, si el rol es 1 redireccionar a la pagina "doctores.html", si no redireccionar a la pagina "admins.html"
        if len(data) == 1:
            if rol == ((1,),):
                # recuperar la contrase;a hasheada de la bd
                cursor.execute('SELECT Password FROM tb_doctores WHERE RFC = %s', (user,))
                contraseña = cursor.fetchone()
                contraseña = contraseña[0]
                # verificar la contraseña
                if contexto.verify(password, contraseña):
                    session['rfc'] = user
                    session['rol'] = doctor
                    # flash con un mensaje de bienvenida y el nombre del usuario
                    flash("Bienvenido dr" + data[0][2])
                    # redireccionar a la ruta /doctores en el archivo "doctor.py"
                    return redirect(url_for('second.doctores'))
                else:
                    flash("Contraseña incorrecta")
                    return render_template('index.html')           
            else:
                # recuperar la contrase;a hasheada de la bd
                cursor.execute('SELECT Password FROM tb_doctores WHERE RFC = %s', (user,))
                contraseña = cursor.fetchone()
                contraseña = contraseña[0]
                # verificar la contraseña
                if contexto.verify(password, contraseña):
                    session['rfc'] = user
                    session['rol'] = admin
                    # flash con un mensaje de bienvenida y el nombre del usuario
                    flash("Bienvenido dr admin " + data[0][2])
                    return redirect(url_for('admins'))
                else:
                    flash("Contraseña incorrecta")
                    return render_template('index.html')
        else:
            flash("Usuario no encontrado")
            return redirect(url_for('index'))
    else:
        flash("si entra aqui me doy un tiro")
        return render_template('index.html')
    

@app.route('/registrar_medico', methods=['GET', 'POST'])
def registrar_medico():
    if request.method == 'POST':
        # obtener los datos del forms
        rfc = request.form['rfc']
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        correo = request.form['correo']
        pass1 = request.form['password']
        confirmacionPass = request.form['confirmacionPass']
        rol = request.form['rol']
        # crear una consulta para verificar los datos
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM tb_doctores WHERE RFC = %s', [rfc])
        # ejeutar la consulta fetchall() para obtener todos los registros
        data = cursor.fetchall()
        # verificar si el usuario existe, si existe verificar su rol, si el rol es 1 redireccionar a la pagina "doctores.html", si no redireccionar a la pagina "admins.html"
        if len(data) == 1:
            flash('El RFC ya esta registrado', 'danger')
            return redirect(url_for('admins'))
        else:
            # comparar las contraseñas
            if pass1 == confirmacionPass:
                pass_hash = contexto.encrypt(pass1)
                # consulta para insertar los datos
                cursor.execute('INSERT INTO tb_doctores (RFC, Nombre, Cedula, Correo, Password, Rol) VALUES (%s, %s, %s, %s, %s, %s)', (rfc, nombre, cedula, correo, pass_hash, rol))
                # guardar los cambios
                mysql.connection.commit()
                flash('El doctor ' + nombre[0:15] + ' ha sido registrado con exito!')
                return redirect(url_for('admins'))
            else:
                flash('Las contraseñas no coinciden', 'danger')
                return redirect(url_for('admins'))

@app.route('/eliminar_medico/<id>')
def eliminar_medico(id):
    # crear una consulta para eliminar el medico
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM tb_doctores WHERE id_doctor = %s', [id])
    # guardar los cambios
    mysql.connection.commit()
    flash('El doctor ha sido eliminado con exito!')
    return redirect(url_for('admins'))
 
@app.route('/editar_medico', methods=['GET', 'POST'])
def editar_medico():
    if request.method == 'POST':
        # obtener los datos del forms
        rfc_nuevo = request.form['rfc_nuevo']
        nombre_nuevo = request.form['nombre_nuevo']
        cedula_nuevo = request.form['cedula_nuevo']
        correo_nuevo = request.form['correo_nuevo']
        pass1_nuevo = request.form['password_nueva']
        confirmacionPass_nuevo = request.form['confirmacionPass_nueva']
        rol_nuevo = request.form['rol_nuevo']

        # verificar las contraseñas que coincidan
        if pass1_nuevo == confirmacionPass_nuevo:
            # encriptar la contraseña nueva pass1_nuevo
            pass_hash = contexto.encrypt(pass1_nuevo)
            # crear una consulta para actualizar los datos
            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE tb_doctores SET RFC = %s, Nombre = %s, Cedula = %s, Correo = %s, Password = %s, Rol = %s WHERE RFC = %s', (rfc_nuevo, nombre_nuevo, cedula_nuevo, correo_nuevo, pass_hash, rol_nuevo, rfc_nuevo))
            # guardar los cambios
            mysql.connection.commit()
            flash('El doctor ha sido editado con exito!')
            return redirect(url_for('admins'))
        else:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(url_for('admins'))
    else: 
        return redirect(url_for('admins'))


@app.route('/registrar_paciente', methods=['GET', 'POST'])
def registrar_paciente():
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
        return redirect(url_for('pacientes'))
    
@app.route('/editar_paciente', methods=['GET', 'POST'])
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
    return redirect(url_for('verPacientes'))

@app.route('/guardar_cita', methods=['GET', 'POST'])
def guardar_cita():
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
            return redirect(url_for('exploracion_diagnostico'))
        else:
            flash('El paciente no existe o no esta relacionado al doctor en sesion!')
            return redirect(url_for('exploracion_diagnostico'))
    else:
        print('no se pudo guardar')
        return redirect(url_for('exploracion_diagnostico'))

@app.route('/receta')
def receta():
    return render_template('receta.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
   # cerrrar la sesión
   session.clear()
   flash("Sesión cerrada")
   return redirect(url_for('index'))


# iniciar servidor
if __name__ == '__main__':
    app.run(port = 3000, debug = True)

