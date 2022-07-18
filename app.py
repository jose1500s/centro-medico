from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask.globals import session

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


# crear una ruta para la raiz de la aplicacion
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # obtener los datos del formulario
        user_name = request.form['rfc']
        user_password = request.form['pass']
        activo = "Activo"
        inactivo = "Inactivo"

        # crear una consulta para verificar el usuario y la contraseña
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM tb_doctores WHERE RFC = %s AND Password = %s", [user_name, user_password])

        if result > 0:
            # si el usuario y la contraseña son correctos
            # inicializar la sesion
            cur = mysql.connection.cursor()
            result = cur.execute("SELECT Nombre FROM tb_doctores WHERE RFC = %s AND Password = %s", [user_name, user_password])
            # si rol = 1, es un doctor y se redirecciona a la pagina doctor.html, si es rol = 2 es medico admin y se redirecciona a la pagina admins.html
            if result > 0:
                cur2 = mysql.connection.cursor()
                result = cur2.execute("SELECT Rol FROM tb_doctores WHERE RFC = %s AND Password = %s", [user_name, user_password])
                rol = cur2.fetchone()
                # cambiar el estado del campo "Estado" a "Activo"
                cur3 = mysql.connection.cursor()
                result = cur3.execute("UPDATE tb_doctores SET Estado = %s WHERE RFC = %s AND Password = %s", [activo, user_name, user_password])
                mysql.connection.commit()

                
                # mensaje de cambiado el estado
                flash('Cambiado el estado a Activo', 'success')

                if rol[0] == 1:
                    # iniciar sesion con el resultado de la consulta
                    session['user'] = cur.fetchone()[0]
                    # mensaje flash con el nombre cortado a 15 caracteres
                    flash('Bienvenido ' + session['user'][:15], 'success')
                    return render_template('doctor.html', sesion = session['user'], rol = rol[0])
                elif rol[0] == 2:
                    # iniciar sesion con el resultado de la consulta
                    session['user'] = cur.fetchone()[0]
                    # mensaje flash con el nombre cortado a 15 caracteres
                    flash('Bienvenido ' + session['user'][:15], 'success')
                    return render_template('admins.html', sesion = session['user'], rol = rol[0])
        else:
            # si el usuario y la contraseña son incorrectos
            flash('Usuario o contraseña incorrectos', 'danger')
            return render_template('index.html')
    else:
        return render_template('index.html')


@app.route('/logout')
def logout():
    # destruir la sesion
    session.clear()
    flash('Sesion cerrada', 'success')
    return redirect(url_for('login'))
    

# iniciar servidor
if __name__ == '__main__':
    app.run(port = 3000, debug = True)

