-- database/schema.sql
-- Sistema de Órdenes de Servicio - Esquema de Base de Datos

-- Crear base de datos (ejecutar en psql o pgAdmin primero)
-- CREATE DATABASE ordenes_servicio;

-- Tabla: Cliente (Cesar León)
CREATE TABLE cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla: Técnico (Daniel Albadawi)
CREATE TABLE tecnico (
    id_tecnico SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    especialidad VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100),
    fecha_contratacion DATE,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla: Equipo (Gabriel Rivas)
CREATE TABLE equipo (
    id_equipo SERIAL PRIMARY KEY,
    nombre_equipo VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    numero_serie VARCHAR(100) UNIQUE,
    id_cliente INTEGER REFERENCES cliente(id_cliente),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla: Servicio (Alejandro Boada)
CREATE TABLE servicio (
    id_servicio SERIAL PRIMARY KEY,
    nombre_servicio VARCHAR(100) NOT NULL,
    descripcion TEXT,
    costo_base DECIMAL(10,2),
    tiempo_estimado_horas INTEGER,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla: Tipo de Orden (Andrés Maldonado)
CREATE TABLE tipo_orden (
    id_tipo_orden SERIAL PRIMARY KEY,
    nombre_tipo VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    requiere_aprobacion BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla: Estatus de Orden (José Fermín)
CREATE TABLE estatus_orden (
    id_estatus SERIAL PRIMARY KEY,
    nombre_estatus VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    color_hex VARCHAR(7) DEFAULT '#000000', -- Para UI
    orden_secuencial INTEGER DEFAULT 0, -- Para flujo de trabajo
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla: Prioridad (Juan Rodríguez)
CREATE TABLE prioridad (
    id_prioridad SERIAL PRIMARY KEY,
    nombre_prioridad VARCHAR(50) NOT NULL UNIQUE,
    nivel INTEGER NOT NULL CHECK (nivel > 0), -- 1=Alta, 2=Media, 3=Baja
    tiempo_respuesta_horas INTEGER, -- SLA
    color_hex VARCHAR(7) DEFAULT '#FF0000',
    activo BOOLEAN DEFAULT TRUE
);

-- Insertar datos iniciales necesarios
INSERT INTO tipo_orden (nombre_tipo, descripcion) VALUES 
    ('Reparación', 'Orden de reparación de equipo'),
    ('Mantenimiento', 'Mantenimiento preventivo o correctivo'),
    ('Instalación', 'Instalación de nuevo equipo'),
    ('Consulta', 'Consulta técnica');

INSERT INTO estatus_orden (nombre_estatus, descripcion, orden_secuencial) VALUES 
    ('Recibida', 'Orden recibida, pendiente de asignación', 1),
    ('Asignada', 'Orden asignada a técnico', 2),
    ('En Proceso', 'Trabajo en curso', 3),
    ('Pendiente Repuesto', 'Esperando repuestos', 4),
    ('Completada', 'Trabajo finalizado', 5),
    ('Entregada', 'Equipo entregado al cliente', 6),
    ('Cancelada', 'Orden cancelada', 99);

INSERT INTO prioridad (nombre_prioridad, nivel, tiempo_respuesta_horas, color_hex) VALUES 
    ('Crítica', 1, 4, '#DC3545'),
    ('Alta', 2, 24, '#FD7E14'),
    ('Media', 3, 72, '#FFC107'),
    ('Baja', 4, 168, '#28A745');