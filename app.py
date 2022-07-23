from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from passlib.context import CryptContext



app = Flask(__name__)

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


@app.route('/doctores')
def doctores():
    return render_template('doctor.html')

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

# Un "middleware" que se ejecuta antes de responder a cualquier ruta. Aquí verificamos si el usuario ha iniciado sesión
@app.before_request
def verificarSesion():
    ruta = request.path
    # Si no ha iniciado sesión y no quiere ir a algo relacionado al login, lo redireccionamos al login
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
        print("el rol fue ", rol)

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
                    return redirect(url_for('doctores'))
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
        return redirect(url_for('index'))
    

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


@app.route('/logout', methods=['GET', 'POST'])
def logout():
   # cerrrar la sesión
   session.clear()
   flash("Sesión cerrada")
   return redirect(url_for('index'))

    
# iniciar servidor
if __name__ == '__main__':
    app.run(port = 3000, debug = True)

