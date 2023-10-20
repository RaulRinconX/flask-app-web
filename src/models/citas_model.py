from database.db import get_db_connection
from .entities.Citas import Citas
from datetime import datetime

class citasModel():

    @classmethod
    def get_citas(self):
        try:
            connection=get_db_connection()
            citas=[]

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM CITA")
                resultset=cursor.fetchall()

                for row in resultset:
                    cita=Citas(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
                    citas.append(cita.to_JSON())
                    
            connection.close()
            return citas
        
        except Exception as e:
            raise Exception(e)
    
    @classmethod
    def get_citas_fecha_actual(self):
        try:
            connection = get_db_connection()
            citas = []

            with connection.cursor() as cursor:
                # Obtener la fecha de hoy en el formato "dd/mm/yyyy"
                fecha_hoy = datetime.now()
                sql = "SELECT * FROM CITA WHERE DATE_TRUNC('day', fecha) = %s"
                # Modificar la consulta SQL para filtrar las citas de hoy
                cursor.execute(sql, (fecha_hoy.date(),))
                resultset = cursor.fetchall()

                for row in resultset:
                    cita = Citas(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                    citas.append(cita.to_JSON())

            connection.close()
            return citas
        except Exception as e:
            raise Exception(e)





