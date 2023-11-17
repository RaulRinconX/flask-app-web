from flask import Flask, render_template, request, flash
from config import config 
from database import db
import psycopg2.extras
import re
import requests
import base64
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet

#Routes
from routes import historias
from routes import citas

app = Flask(__name__)

conn = db.get_db_connection()

clave = b'K1ncH8Wws87y3JcwSSpcD9Ot_61a33IV4qNeQgZ9IfU='  # Usa tu clave segura aquí
fernet = Fernet(clave)

@app.route("/")
def index():
     return render_template('index.html')

@app.route("/signup/", methods=['GET', 'POST'])
def show_signup_form():

     cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

     if request.method == 'POST' and 'name' in request.form and 'lastname' in request.form and 'cedula' in request.form and 'birthdate' in request.form and 'bloodtype' in request.form and 'email' in request.form and 'password' in request.form:
          name = request.form['name']
          lastname = request.form['lastname']
          cedula = request.form['cedula']
          birthdate = request.form['birthdate']
          bloodtype = request.form['bloodtype']
          email = request.form['email']
          password = request.form['password']

          hashed_password = generate_password_hash(password)
          
          cursor.execute('SELECT * FROM paciente WHERE correo_electronico = %s', (email,) )
          account = cursor.fetchone()
          print(account)
          if account:
               flash("Account already exists! Please log in.")
          elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
               flash('Invalid email address')
          elif not email or not password or not name or not lastname or not cedula or not birthdate or not bloodtype:
               flash('Please fill out the form')
          else:
               cursor.execute("INSERT INTO paciente (nombre, apellido, correo_electronico, identificacion, fecha_nacimiento, grupo_sanguineo, activo, contraseña_hash, contraseña_salt, historia_medica) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (name, lastname, email, cedula, birthdate, bloodtype, True, hashed_password, hashed_password, 1))
               conn.commit()
               flash('You have successfully registered')
     elif request.method == 'POST':
          flash('Please fill out the form')
     return render_template("auth/signup.html")

@app.route("/login", methods=['GET', 'POST'])
def iniciar_sesion():
     return render_template('auth/login.html')

@app.route("/health-check/")
def health():
    return "OK!"

@app.route("/historias-clinicas/", methods=["GET","POST"])
def agregar_historia_clinica():
     if request.method == 'POST':
          # Obtener datos del formulario
          nombre = request.form['nombre']
          cedula = request.form['cedula']
          fecha_nacimiento = request.form['fecha_nacimiento']
          tipo_sangre = request.form['tipo_sangre']
          fecha_examen = request.form['fecha_examen']
          enfermedades = request.form['enfermedades']
          medicamentos = request.form['medicamentos']
          alergia = request.form['alergia']

          # Encriptar los datos
          nombre_cifrado = base64.urlsafe_b64encode(fernet.encrypt(nombre.encode())).decode('utf-8')
          cedula_cifrada = int(cedula)
          fecha_nacimiento_cifrada = fecha_nacimiento
          tipo_sangre_cifrado = base64.urlsafe_b64encode(fernet.encrypt(tipo_sangre.encode())).decode('utf-8')
          fecha_examen_cifrada = fecha_examen
          enfermedades_cifradas = base64.urlsafe_b64encode(fernet.encrypt(enfermedades.encode())).decode('utf-8')
          medicamentos_cifrados = base64.urlsafe_b64encode(fernet.encrypt(medicamentos.encode())).decode('utf-8')
          alergia_cifrada = base64.urlsafe_b64encode(fernet.encrypt(alergia.encode())).decode('utf-8')

          # Insertar en la base de datos
          conn = db.get_db_connection()
          cur = conn.cursor()
          cur.execute('INSERT INTO historias (nombre, cedula, fecha_nacimiento, tipo_sangre, fecha_examen, enfermedades, medicamentos, alergia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                         (nombre_cifrado, cedula_cifrada, fecha_nacimiento_cifrada, tipo_sangre_cifrado, fecha_examen_cifrada, enfermedades_cifradas, medicamentos_cifrados, alergia_cifrada))
          conn.commit()
          conn.close()
     url ='http://34.160.204.45:80/api/historias-clinicas'
     response = requests.get(url)
     data = response.json()
     return render_template('auth/historias.html',json_data=data)

def page_not_found(error):
     return "<h1> Not found page :( </h1>",404

def unauthorized(error):
     return "<h1> No tienes permisos >:( </h1>",401

if __name__ == "__main__":
      app.config.from_object(config['development'])

      #Blueprints
      app.register_blueprint(historias.main, url_prefix='/api/historias-clinicas/')
      app.register_blueprint(citas.main, url_prefix='/api/citas/')

      #ErrorHandlers
      app.register_error_handler(404, page_not_found)
      app.register_error_handler(401, unauthorized)
      app.run(host='0.0.0.0', port=8080, debug=True)
