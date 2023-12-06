from flask import Flask, redirect, render_template, request, flash, url_for, session, make_response
from functools import wraps
from psycopg2.errors import UniqueViolation
import psycopg2.extras
from config import config
from database import db
import re
import requests
import base64
from werkzeug.security import generate_password_hash, check_password_hash
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os

from urllib.parse import urlencode





app = Flask(__name__)

conn = db.get_db_connection()

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
    jwks_uri='https://' + os.getenv('AUTH0_DOMAIN') + '/.well-known/jwks.json',
)


@app.route("/usuarios")
def index():
    return render_template('index.html')

def requires_auth_role(role):
    def requires_role_decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'profile' not in session or (role not in session.get('roles', [])):
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated
    return requires_role_decorator


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
            "client_id": os.getenv('AUTH0_CLIENT_ID'),
            "client_secret": os.getenv('AUTH0_CLIENT_SECRET'),
            "audience": f'https://{os.getenv("AUTH0_DOMAIN")}/api/v2/',
            "grant_type": "client_credentials"
        })

        if auth0_response.status_code != 200:
            flash('Error obtaining token from Auth0')
            print(auth0_response.json())
            return render_template("auth/signup.html")

        access_token = auth0_response.json()['access_token']

        # Call Auth0 API to create user
        response = requests.post(f'https://{os.getenv("AUTH0_DOMAIN")}/api/v2/users', json=data,
                                headers={'Authorization': f'Bearer {access_token}'})

        print(response.status_code)
        print(response.json())
        if response.status_code == 201 or response.status_code == 200:
            # Call Auth0 API to create user
            try:
                cursor.execute("INSERT INTO paciente (nombre, apellido, correo_electronico, identificacion, fecha_nacimiento, grupo_sanguineo, activo, contraseña_hash, contraseña_salt) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (name, lastname, email, cedula, birthdate, bloodtype, True, hashed_password, hashed_password))
                conn.commit()
                flash('You have successfully registered')
                return redirect(url_for('iniciar_sesion'))
            except UniqueViolation:
                # Handle duplicate user error
                flash('User already exists')
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


@app.route("/health-check")
def health():
    return "OK!"

@app.route('/callback/')
def callback_handling():
    # Maneja la respuesta de autenticación de Auth0
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Establecer la sesión del usuario
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo.get('name', ''),
        'picture': userinfo.get('picture', ''),
    }

    auth0_response = requests.post(f'https://{os.getenv("AUTH0_DOMAIN")}/oauth/token', json={
            "client_id": os.getenv('AUTH0_CLIENT_ID'),
            "client_secret": os.getenv('AUTH0_CLIENT_SECRET'),
            "audience": f'https://{os.getenv("AUTH0_DOMAIN")}/api/v2/',
            "grant_type": "client_credentials"
        })

    if auth0_response.status_code != 200:
        flash('Error obtaining token from Auth0')
        print(auth0_response.json())
        return redirect(url_for('iniciar_sesion'))

    access_token = auth0_response.json()['access_token']

    user_id = userinfo['sub']
    headers = {'Authorization': f'Bearer {access_token}'}
    roles_url = f'https://{os.getenv("AUTH0_DOMAIN")}/api/v2/users/{user_id}/roles'
    roles_response = requests.get(roles_url, headers=headers)

    if roles_response.status_code == 200 or roles_response.status_code == 201:
        roles_data = roles_response.json()
        session['roles'] = [role['name'] for role in roles_data]
        print(session['roles'])
        print("Roles obtenidos de Auth0")
        print(roles_response.json())
    else:
        print(roles_response.json())
        print("Error getting roles from Auth0")

    response = make_response(redirect(url_for('index')))
    # le pasa los roles a fastapi, de manera segura
    response.set_cookie('session_id', session['roles'][0], httponly=True, samesite='Lax')
    return response


@app.route('/logout')
def logout():
    # Limpiar la sesión de Flask
    session.clear()

    # Crear la URL de logout de Auth0
    params = {'returnTo': url_for('index', _external=True), 'client_id': os.getenv('AUTH0_CLIENT_ID')}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


def page_not_found(error):
    return "<h1> Not found page :( </h1>",404

def unauthorized(error):
    return "<h1> No tienes permisos >:( </h1>",401


if __name__ == "__main__":
    app.config.from_object(config['development'])

    #ErrorHandlers
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(401, unauthorized)
    app.run(host='0.0.0.0', port=8080, debug=True)
