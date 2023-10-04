class Historias():

    def __init__(self,id,nombre,cedula,fecha_nacimiento,tipo_sangre,fecha_examen,enfermedades,medicamentos,alergia) -> None:
        self.id = id
        self.nombre = nombre
        self.cedula = cedula
        self.fecha_nacimiento = fecha_nacimiento
        self.tipo_sangre = tipo_sangre
        self.fecha_examen = fecha_examen
        self.enfermedades = enfermedades
        self.medicamentos = medicamentos
        self.alergia = alergia
    
    def to_JSON(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'cedula': self.cedula,
            'fecha_nacimiento': self.fecha_nacimiento,
            'tipo_sangre': self.tipo_sangre,
            'fecha_examen': self.fecha_examen,
            'enfermedades': self.enfermedades,
            'medicamentos': self.medicamentos,
            'alergia': self.alergia
        }