# 📊 Análisis del Proyecto - Sistema de Órdenes de Servicio

## 🏗️ Arquitectura del Sistema

Tu proyecto sigue una **arquitectura en capas** con el patrón **MVC (Modelo-Vista-Controlador)**:

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                      │
│              (Templates HTML - Flask/Jinja2)                 │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                   CAPA DE CONTROLADORES                      │
│     (cliente_controller.py, equipo_controller.py, ...)       │
│           Manejan las peticiones HTTP (routes)               │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                   CAPA DE SERVICIOS                          │
│     (cliente_service.py, equipo_service.py, ...)             │
│       Lógica de negocio, validaciones, reglas                │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                   CAPA DE DAO (Data Access)                  │
│        (cliente_dao.py, equipo_dao.py, ...)                  │
│      Acceso a base de datos, queries SQL                     │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                   CAPA DE MODELOS                            │
│         (cliente.py, equipo.py, ...)                         │
│      Entidades/Objetos de dominio                            │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                   BASE DE DATOS                              │
│              PostgreSQL + psycopg2                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Estructura de Carpetas

```
Sistema_Ordenes_Servicios/
├── app/
│   ├── __init__.py              # Inicialización de Flask
│   ├── config.py                # Configuración de BD
│   │
│   ├── controllers/             # 🎮 Controladores (Routes)
│   │   ├── cliente_controller.py
│   │   ├── equipo_controller.py
│   │   ├── tecnico_controller.py
│   │   ├── servicio_controller.py
│   │   ├── tipo_orden_controller.py
│   │   ├── estatus_orden_controller.py
│   │   ├── prioridad_controller.py
│   │   └── main_controller.py
│   │
│   ├── services/                # ⚙️ Lógica de Negocio
│   │   ├── base_service.py      # Clase base con CRUD genérico
│   │   ├── cliente_service.py
│   │   ├── equipo_service.py
│   │   ├── tecnico_service.py
│   │   ├── servicio_service.py
│   │   ├── tipo_orden_service.py
│   │   ├── estatus_orden_service.py
│   │   └── prioridad_service.py
│   │
│   ├── dao/                     # 💾 Acceso a Datos
│   │   ├── conexion.py          # Conexión PostgreSQL (Singleton)
│   │   ├── base_dao.py          # Clase base con operaciones CRUD
│   │   ├── cliente_dao.py
│   │   ├── equipo_dao.py
│   │   ├── tecnico_dao.py
│   │   ├── servicio_dao.py
│   │   ├── tipo_orden_dao.py
│   │   ├── estatus_orden_dao.py
│   │   └── prioridad_dao.py
│   │
│   ├── models/                  # 📦 Modelos/Entidades
│   │   ├── cliente.py
│   │   ├── equipo.py
│   │   ├── tecnico.py
│   │   ├── servicio.py
│   │   ├── tipo_orden.py
│   │   ├── estatus_orden.py
│   │   └── prioridad.py
│   │
│   └── templates/               # 🎨 Vistas HTML
│       └── cliente/
│           ├── listar.html
│           ├── crear.html
│           ├── editar.html
│           └── ver.html
│
├── database/
│   └── schema.sql               # 📋 Esquema de BD
│
├── run.py                       # 🚀 Punto de entrada
└── requirements.txt             # 📦 Dependencias
```

---

## 🔄 Flujo de Crear Cliente (Caso de Uso)

```
Usuario
   │
   │ 1. POST /clientes/nuevo (formulario)
   ▼
┌──────────────────────────────────────────┐
│  cliente_controller.crear_cliente()      │
│  - Recibe datos del formulario           │
│  - Prepara diccionario con datos         │
└──────────────────────────────────────────┘
   │
   │ 2. cliente_service.crear(datos)
   ▼
┌──────────────────────────────────────────┐
│  cliente_service.crear()                 │
│  - Valida datos (validar_datos)          │
│  - Verifica duplicados (cedula)    ← ERROR AQUÍ
│  - Llama a DAO para insertar             │
└──────────────────────────────────────────┘
   │
   │ 3. cliente_dao.insertar(datos)
   ▼
┌──────────────────────────────────────────┐
│  cliente_dao.insertar()                  │
│  - Construye query INSERT                │
│  - Ejecuta en PostgreSQL                 │
└──────────────────────────────────────────┘
   │
   │ 4. Retorna ID del nuevo cliente
   ▼
Usuario ve mensaje de éxito
```

---

## 📋 Entidades del Sistema

| Entidad | Responsable | Tabla BD | Estado |
|---------|-------------|----------|--------|
| **Cliente** | Cesar León | `cliente` | ⚠️ Tiene error |
| **Técnico** | Daniel Albadawi | `tecnico` | ✅ OK |
| **Equipo** | Gabriel Rivas | `equipo` | ✅ OK |
| **Servicio** | Alejandro Boada | `servicio` | ✅ OK |
| **Tipo Orden** | Andrés Maldonado | `tipo_orden` | ✅ OK |
| **Estatus Orden** | José Fermín | `estatus_orden` | ✅ OK |
| **Prioridad** | Juan Rodríguez | `prioridad` | ✅ OK |

---

## 🔧 Patrones de Diseño Usados

### 1. **DAO (Data Access Object)**
- Separa la lógica de acceso a datos del resto de la aplicación
- `base_dao.py` tiene métodos CRUD genéricos
- Cada entidad tiene su propio DAO que hereda de BaseDAO

### 2. **Singleton**
- `ConexionDB` es un singleton - solo existe una instancia de conexión
- Garantiza una única conexión a PostgreSQL

### 3. **Service Layer**
- Capa intermedia entre controladores y DAOs
- Contiene la lógica de negocio y validaciones
- Permite reutilizar lógica entre diferentes controladores

### 4. **Template Method**
- `BaseService` define el flujo de operaciones CRUD
- Las subclases implementan validaciones específicas

---

## 📊 Base de Datos - Tablas

### Tabla: `cliente`
```sql
CREATE TABLE cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) UNIQUE NOT NULL,  -- ← FALTABA ESTA COLUMNA
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);
```

### Tabla: `tecnico`
```sql
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
```

### Tabla: `equipo`
```sql
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
```

### Tablas de Catálogos (datos iniciales incluidos)
- `servicio` - Tipos de servicios ofrecidos
- `tipo_orden` - Tipos: Reparación, Mantenimiento, Instalación, Consulta
- `estatus_orden` - Estados: Recibida, Asignada, En Proceso, etc.
- `prioridad` - Niveles: Crítica, Alta, Media, Baja

---

## ✅ Casos de Uso Implementados (CU-G)

| Código | Caso de Uso | Estado |
|--------|-------------|--------|
| CU-G01 | Crear entidad | ✅ Implementado |
| CU-G02 | Listar entidades | ✅ Implementado |
| CU-G03 | Actualizar entidad | ✅ Implementado |
| CU-G04 | Eliminar entidad | ✅ Implementado |
| CU-G05 | Buscar entidad | ✅ Implementado |

---

## 🚀 Cómo Ejecutar el Proyecto

```bash
# 1. Activar entorno virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar base de datos en app/config.py
# O crear archivo .env con:
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=ordenes_servicio
# DB_USER=tu_usuario
# DB_PASSWORD=tu_password

# 4. Ejecutar migración para corregir tabla cliente
python ejecutar_migracion.py

# 5. Iniciar aplicación
python run.py

# 6. Abrir en navegador
http://localhost:5000
```

---

## 🎯 Próximos Pasos Sugeridos

1. ✅ **Corregir el error de la columna cedula** (prioridad alta)
2. 🎨 **Crear templates HTML** para todas las entidades
3. 🔐 **Agregar autenticación** (login/logout)
4. 📄 **Crear tabla orden_servicio** (entidad principal del sistema)
5. 📊 **Agregar reportes y dashboards**
6. 🧪 **Crear pruebas unitarias**

---

## 📚 Tecnologías Usadas

| Tecnología | Versión | Uso |
|------------|---------|-----|
| Python | 3.x | Lenguaje principal |
| Flask | 3.x | Framework web |
| PostgreSQL | 14+ | Base de datos |
| psycopg2 | 2.9+ | Driver PostgreSQL |
| Jinja2 | 3.x | Templates HTML |
| python-dotenv | 1.x | Variables de entorno |

---

## 👥 Equipo de Desarrollo

- **Cesar León** - Cliente
- **Daniel Albadawi** - Técnico
- **Gabriel Rivas** - Equipo
- **Alejandro Boada** - Servicio
- **Andrés Maldonado** - Tipo Orden
- **José Fermín** - Estatus Orden
- **Juan Rodríguez** - Prioridad

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en la consola
2. Verifica la conexión a PostgreSQL
3. Confirma que las tablas existen con la estructura correcta
4. Revisa que los permisos de usuario sean correctos
