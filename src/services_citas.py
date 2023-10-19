from flask import Flask, request, jsonify
from flask_mail import Mail, Message

app = Flask(__name)

# Configuración de Flask-Mail
app.EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
app.EMAIL_HOST = 'smtp.office365.com'
app.EMAIL_USE_TLS = True
app.EMAIL_PORT = 587
app.EMAIL_HOST_USER = 'aykutrincon@gmail.com'
app.EMAIL_HOST_PASSWORD = 'scfuiloumslnoaah'

mail = Mail(app)

@app.route('/enviar_correo', methods=['POST'])
def enviar_correo():
    if request.method == 'POST':
        try:
            data = request.get_json()

            subject = data.get('subject')
            recipients = data.get('recipients')
            message_body = data.get('message_body')

            message = Message(subject=subject, recipients=recipients, body=message_body)
            mail.send(message)

            return jsonify({"message": "Correo enviado exitosamente"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Método de solicitud no válido"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)