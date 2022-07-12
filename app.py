from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
# crear una ruta para la raiz de la aplicacion
@app.route('/')
def index():
    return render_template('index.html')

# iniciar servidor
if __name__ == '__main__':
    app.run(port = 3000, debug = True)