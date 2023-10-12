from flask import Flask, render_template, request
from config import config 
from database import db
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
#Routes
from routes import historias

app = Flask(__name__)

#conn = db.get_db_connection()

@app.route("/")
def index():
     return render_template('index.html')

@app.route("/signup/")
def show_signup_form():
     return render_template("signup_form.html")

@app.route("/login", methods=['GET', 'POST'])
def iniciar_sesion():
     #cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
     if request.method == 'POST':
          username = request.form['username']
          password = request.form['password']
          hashed_password = generate_password_hash(password)
          #cursor.execute('SELECT * FROM users WHERE username = %s', (username,) )
          #account = cursor.fetchone()
          #if account:
              # print("melo")
          #else:
               #cursor.execute("INSERT INTO users (username, password) VALUES (%s,%s)", (username, hashed_password))
               #conn.commit()
               #print("no tan melo")
     else:
          return render_template('auth/login.html')

@app.route("/health-check/")
def health():
    return "OK!"

@app.route("/historias-clinicas/")
def consultar_historias():
     return "hola"

def page_not_found(error):
     return "<h1> Not found page :( </h1>",404

def unauthorized(error):
     return "<h1> No tienes permisos >:( </h1>",401

if __name__ == "__main__":
      app.config.from_object(config['development'])

      #Blueprints
      app.register_blueprint(historias.main, url_prefix='/api/historias')

      #ErrorHandlers
      app.register_error_handler(404, page_not_found)
      app.register_error_handler(401, unauthorized)
      app.run(host='0.0.0.0', port=8080)
