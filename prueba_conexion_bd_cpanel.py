import pymysql

# --- DATOS DE CONEXIÓN ---
# En host usa la IP de tu servidor cPanel o el dominio de tu sitio web
HOST = "crsensores.com"  # o la IP del servidor (ej. '192.168.1.1')
USUARIO = "crsensor_harol"  # El usuario que asignaste en cPanel (ej: miusuario_admin)
PASSWORD = "bd_4dm1n2026+"  # La contraseña de ese usuario
BASE_DATOS = "crsensor_clientes"  # Nombre de la base de datos (ej: miusuario_mibasedatos)
PUERTO = 3306  # Puerto MySQL estándar

try:
    # Establecer la conexión
    conexion = pymysql.connect(
        host=HOST,
        user=USUARIO,
        password=PASSWORD,
        database=BASE_DATOS,
        port=PUERTO,
        charset="utf8mb4",
    )

    print("¡Conexión exitosa a la base de datos de cPanel!")

    # Probar una consulta rápida (opcional)
    with conexion.cursor() as cursor:
        cursor.execute("SELECT VERSION();")
        version = cursor.fetchone()
        print(f"Versión de MySQL/MariaDB: {version[0]}")

    conexion.close()

except pymysql.MySQLError as e:
    print(f"Error al conectar a la base de datos: {e}")