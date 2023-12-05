CREATE TABLE public.usuario (
    usuario_id SERIAL PRIMARY KEY,
    nombre VARCHAR(255),
    apellido VARCHAR(255),
    correo_electronico VARCHAR(255) UNIQUE,
    fecha_nacimiento DATE,
    fecha_registro TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    activo BOOLEAN DEFAULT true,
    contraseña_hash VARCHAR(255),
    contraseña_salt VARCHAR(255)
);

CREATE TABLE public.paciente (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    correo_electronico VARCHAR(255) NOT NULL UNIQUE,
    identificacion VARCHAR(20) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    grupo_sanguineo VARCHAR(3) NOT NULL,
    activo BOOLEAN NOT NULL,
    contraseña_hash VARCHAR(255) NOT NULL,
    contraseña_salt VARCHAR(255) NOT NULL
);
