# Catálogos de órdenes de servicio — Flask y PostgreSQL

Aplicación académica con capas de controlador, servicio, DAO y entidades. Gestiona clientes, técnicos, equipos, servicios, tipos de orden, estatus y prioridades. El esquema actual contiene siete catálogos; todavía no incluye una entidad de orden, asignación completa de trabajos, autenticación ni autorización de usuarios. Debe presentarse con ese alcance.

## Inicio local

Python3.11+ y PostgreSQL16. Crear una base **nueva de desarrollo**, separada de cualquier base institucional, y aplicar `database/schema.sql` únicamente en ella. Configurar un `.env` local con `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` y una `SECRET_KEY` aleatoria. No publicar ese archivo ni usar las migraciones sobre una base existente sin respaldo y revisión.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe run.py
```

El servidor escucha en `127.0.0.1:5000`, con debug apagado por defecto. Se leen variables solamente desde el `.env` de esta carpeta, sin buscar archivos privados de otras carpetas. No hay contraseña de BD predeterminada; la clave de sesión se genera si no se configura, y cambia al reiniciar.

## Pruebas

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

18 pruebas de lógica, consultas y HTTP funcionan sin PostgreSQL real. Comprueban formularios CSRF, cabeceras, hosts confiables, valores numéricos finitos, identifiers SQL, errores internos, conexiones aisladas por hilo y fallback de encoding. Dos pruebas adicionales requieren un clúster sintético explícito: loopback55432 y base cuyo nombre empieza con `portfolio_orders_synthetic`. Para ese entorno únicamente:

```powershell
$env:RUN_SYNTHETIC_PG_TESTS='1'
.\.venv\Scripts\python.exe -m pytest -q
```

Verificado el7 de octubre de2026 en Windows/Python3.14.3:20 pruebas correctas, incluyendo CRUD real de cliente con desactivación lógica, creación de servicio con costo decimal y rechazo de NaN. El clúster nuevo se creó en `.local-db/` con autenticación SCRAM y datos ficticios; no se usaron servicios PostgreSQL existentes ni puerto5432. `.env`, datos del clúster, venv y logs están ignorados por Git. CI utiliza únicamente las pruebas sin base externa.

## Cambios de seguridad y límites

- Todos los21 formularios POST incluyen token CSRF, verificado antes de ejecutar el controlador.
- Cookies HttpOnly/SameSite, no-store, protección de frames/MIME y cuerpo máximo de1MiB.
- Conexión por hilo con cierre al terminar request y timeout de conexión.
- Columnas SQL dinámicas se validan también al insertar/actualizar; los valores permanecen parametrizados.
- Errores internos se registran localmente y no se muestran como detalles SQL al visitante.
- Costos NaN/infinito se rechazan.
- Actualizados python-dotenv1.2.4 y Werkzeug3.1.9 después de hallazgos de pip-audit; auditoría final sin vulnerabilidades conocidas en las dependencias fijadas.

Esto no convierte la aplicación en un servicio público seguro: faltan login/roles, restricciones de acceso a registros, paginación general, registro de actividad y flujo de órdenes. Algunos DAOs específicos todavía manejan cursores directamente; el cierre de conexión por request limita su duración, pero conviene consolidar esa capa. El fallback LATIN1 conserva compatibilidad con bases heredadas; no repara una codificación incorrecta del servidor. La UI académica actual se conserva.

No exponer datos personales o institucionales. Para una demo usar nombres ficticios, IDs de prueba y direcciones `example.invalid`. Las pruebas registran únicamente datos sintéticos y no borran registros originales.

## Lecturas con errores de decoding envueltos

Las lecturas DAO admiten un solo retry cuando un UnicodeDecodeError aparece dentro de `__cause__`/`__context__` o un wrapper no SQL conserva el mensaje explícito de decoding UTF-8. Los ciclos de excepciones terminan y los errores SQL normales no se reintentan por contener texto similar. No se reconecta ni se modifica el aislamiento por hilo.

Antes del retry se cierra el cursor y se hace rollback, conforme al fallback existente. El encoding real de la conexión se restaura al finalizar, incluso si falla el segundo intento; si no se puede restaurar, se descarta esa conexión. El fallback no repara datos mal codificados y puede cambiar cómo se interpreta texto heredado. Conserva las validaciones SQL y los mensajes públicos genéricos.

Validación de esta corrección: 32 pruebas offline aprobadas y dos PostgreSQL omitidas sin activación explícita. Incluye 14 casos nuevos de wrappers, causas/contextos, errores SQL, ciclos, cierre de recursos y restauración. Si una cadena contiene un error SQL, el texto del wrapper no basta para reintentar: se exige un UnicodeDecodeError real. Referencia de la API de encoding: [Psycopg connection](https://www.psycopg.org/docs/connection.html#connection.encoding).

La validación dirigida posterior creó otro clúster PostgreSQL 16.2 sintético y ejecutó las 34 pruebas, incluidas las dos opt-in. Una comprobación adicional contra esa conexión real inyectó un wrapper ficticio durante `SELECT 'synthetic'` y confirmó restauración UTF8→fallback→UTF8; no se afirma que PostgreSQL produjera naturalmente bytes inválidos. El clúster de prueba se detuvo al finalizar. CI conserva la suite offline y añade un job de PostgreSQL 16 descartable, limitado a loopback y con credencial efímera de demo, que aplica el esquema y ejecuta las dos integraciones. No usa datos institucionales ni credenciales locales.
