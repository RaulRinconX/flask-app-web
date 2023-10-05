from flask import Flask, render_template
from config import config 

#Routes
from routes import historias

app = Flask(__name__)

@app.route("/")
def index():
     return render_template('index.html')
@app.route("/signup/")
def show_signup_form():
     return render_template("signup_form.html")
@app.route("/login")
def iniciar_sesion():
     return render_template('login.html')
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
