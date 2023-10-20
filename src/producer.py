import time
import pika
import requests
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'aykutrincon@gmail.com'
EMAIL_HOST_PASSWORD = 'scfuiloumslnoaah'

print('> Sending citas. To exit press CTRL+C')

url = 'http://34.160.204.45:80/api/citas-actual'

while True:
    response = requests.get(url)
    data = response.json()

    current_time = datetime.now()

    for cita in data:
        fecha_cita = datetime.strptime(cita['fecha'], '%d/%m/%Y %H:%M:%S')
        two_hours_later = current_time + timedelta(hours=2)
        recipient_email = cita['correo_paciente']

        if fecha_cita <= two_hours_later:
            # Envía un correo a la persona
            subject = 'Recordatorio de cita'
            message = f'Esto es un recordatorio de su cita: {cita}'
            from_email = 'aykutrincon@gmail.com'

            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            server.starttls()
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            text = msg.as_string()
            server.sendmail(from_email, recipient_email, text)
            server.quit()

            print(f"Correo enviado para la cita: {cita}")

    time.sleep(5)