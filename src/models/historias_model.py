from database.db import get_db_connection
from .entities.Historias import Historias

class historiaModel():

    @classmethod
    def get_historias(self):
        try:
            connection=get_db_connection()
            historias=[]

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM HISTORIAS ORDER BY ID")
                resultset=cursor.fetchall()

                for row in resultset:
                    historia=Historias(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                    historias.append(historia.to_JSON())
            connection.close()
            return historias
        except Exception as e:
            raise Exception(e)