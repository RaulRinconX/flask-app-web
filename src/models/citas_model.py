from database.db import get_db_connection
from .entities.Citas import Citas

class citasModel():

    @classmethod
    def get_citas(self):
        try:
            connection=get_db_connection()
            citas=[]

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM CITAS")
                resultset=cursor.fetchall()

                for row in resultset:
                    cita=Citas(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                    citas.append(cita.to_JSON())
                    
            connection.close()
            return citas
        
        except Exception as e:
            raise Exception(e)