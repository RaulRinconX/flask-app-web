from utils.dateformat import DateFormat

class Citas():

    def __init__(self,id,id_paciente,correo_paciente,id_profesional,fecha,especialidad,estado,precio) -> None:
        self.id = id
        self.id_paciente = id_paciente
        self.correo_paciente = correo_paciente
        self.id_profesional = id_profesional
        self.fecha = fecha
        self.especialidad = especialidad
        self.estado = estado
        self.precio =  precio
    
    def to_JSON(self):
        return {
            'id': self.id,
            'id_paciente': self.id_paciente,
            'correo_paciente': self.correo_paciente,
            'id_profesional': self.id_profesional,
            'fecha': DateFormat.convert_date_hour(self.fecha),
            'especialidad': self.especialidad,
            'estado': self.estado,
            'precio': self.precio
        }