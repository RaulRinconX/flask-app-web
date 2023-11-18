from flask import Flask, redirect, render_template, request, flash, url_for
from config import config 
from database import db
import psycopg2.extras
import re
import requests
import base64
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet, InvalidToken

#Routes
from routes import historias
from routes import citas

#Auth0
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os





app = Flask(__name__)

conn = db.get_db_connection()

clave = b'K1ncH8Wws87y3JcwSSpcD9Ot_61a33IV4qNeQgZ9IfU='  # Usa tu clave segura aquí
fernet = Fernet(clave)

load_dotenv()

oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
   client_secret=os.getenv('AUTH0_CLIENT_SECRET'),
    api_base_url='https://' + os.getenv("AUTH0_DOMAIN"),
    access_token_url= 'https://' + os.getenv("AUTH0_DOMAIN") + '/oauth/token',
    authorize_url= 'https://' + os.getenv("AUTH0_DOMAIN") + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    }, client_id=os.getenv('AUTH0_CLIENT_ID'),
    
)


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

          # Prepare data for Auth0 API
          data = {
               'email': email,
               'password': password,
               'connection': 'Username-Password-Authentication'  # Adjust as necessary
          }

          hashed_password = generate_password_hash(password)

          auth0_response = requests.post(f'https://{os.getenv("AUTH0_DOMAIN")}/oauth/token', json={
               "client_id": "YOUR_CLIENT_ID",
               "client_secret": "YOUR_CLIENT_SECRET",
               "audience": f'https://{os.getenv("AUTH0_DOMAIN")}/api/v2/',
               "grant_type": "client_credentials"
          })

          if auth0_response.status_code != 200:
               flash('Error obtaining token from Auth0')
               return render_template("auth/signup.html")

          access_token = auth0_response.json()['access_token']

          # Call Auth0 API to create user
          response = requests.post(f'https://{os.getenv("AUTH0_DOMAIN")}/api/v2/users', json=data,
                                   headers={'Authorization': f'Bearer {access_token}'})
          
          if response.status_code == 201:
               # Call Auth0 API to create user
               try:
                    cursor.execute("INSERT INTO paciente (nombre, apellido, correo_electronico, identificacion, fecha_nacimiento, grupo_sanguineo, activo, contraseña_hash, contraseña_salt, historia_medica) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (name, lastname, email, cedula, birthdate, bloodtype, True, hashed_password, hashed_password, 1))
                    conn.commit()
                    flash('You have successfully registered')
               except psycopg2.errors.UniqueViolation:
                    flash("Account already exists! Please log in.")
          else:
            # Handle Auth0 API error
            flash('Error creating user in Auth0')

     elif request.method == 'POST':
          flash('Please fill out the form')
     return render_template("auth/signup.html")

# @app.route("/login", methods=['GET', 'POST'])
# def iniciar_sesion():
#      return render_template('auth/login.html')

@app.route('/login')
def iniciar_sesion():
    return auth0.authorize_redirect(redirect_uri=os.getenv('AUTH0_CALLBACK_URL'))


@app.route("/health-check/")
def health():
    return "OK!"

@app.route("/historias-clinicas/", methods=["GET","POST"])
def agregar_historia_clinica():
     if request.method == 'POST' and 'nombre' in request.form and 'cedula' in request.form and 'fecha_nacimiento' in request.form and 'tipo_sangre' in request.form and 'fecha_examen' in request.form and 'enfermedades' in request.form and 'medicamentos' in request.form and 'alergia' in request.form:
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
          cedula_cifrada = base64.urlsafe_b64encode(fernet.encrypt(cedula.encode())).decode('utf-8')
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
          return redirect(url_for('agregar_historia_clinica'))
     url ='http://34.160.204.45:80/api/historias-clinicas'
     response = requests.get(url)
     historias_cifradas = response.json()
     # Desencriptar los datos
     historias = []
     for historia_cifrada in historias_cifradas:
          try:
               historia = {
                    'nombre': fernet.decrypt(base64.urlsafe_b64decode(historia_cifrada['nombre'])).decode('utf-8'),
                    'cedula': fernet.decrypt(base64.urlsafe_b64decode(historia_cifrada['cedula'])).decode('utf-8'),
                    'fecha_nacimiento': historia_cifrada['fecha_nacimiento'],  # Suponiendo que esta no está cifrada
                    'tipo_sangre': fernet.decrypt(base64.urlsafe_b64decode(historia_cifrada['tipo_sangre'])).decode('utf-8'),
                    'fecha_examen': historia_cifrada['fecha_examen'],  # Suponiendo que esta no está cifrada
                    'enfermedades': fernet.decrypt(base64.urlsafe_b64decode(historia_cifrada['enfermedades'])).decode('utf-8'),
                    'medicamentos': fernet.decrypt(base64.urlsafe_b64decode(historia_cifrada['medicamentos'])).decode('utf-8'),
                    'alergia': fernet.decrypt(base64.urlsafe_b64decode(historia_cifrada['alergia'])).decode('utf-8')
               }
               historias.append(historia)
          except (InvalidToken, TypeError, base64.binascii.Error):
               # Manejar el error si la desencriptación falla
               # Esto puede suceder si el token es inválido o si los datos no están correctamente codificados en base64
               pass

     # Renderizar la plantilla con los datos desencriptados
     return render_template('auth/historias.html', json_data=historias)
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
