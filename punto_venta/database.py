import sqlite3

DB_NAME = "ventas.db"


def conectar():
    return sqlite3.connect(DB_NAME)


def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        hora TEXT NOT NULL,
        producto TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL,
        total REAL NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gastos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        hora TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        monto REAL NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        rol TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def insertar_producto(nombre, precio):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, precio) VALUES (?, ?)",
        (nombre, precio)
    )
    conn.commit()
    conn.close()


def obtener_productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, precio FROM productos")
    datos = cursor.fetchall()
    conn.close()
    return datos


def eliminar_producto(id_producto):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
    conn.commit()
    conn.close()


def insertar_venta(fecha, hora, producto, cantidad, precio, total):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ventas (fecha, hora, producto, cantidad, precio, total)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (fecha, hora, producto, cantidad, precio, total))
    conn.commit()
    conn.close()


def obtener_ventas_del_dia(fecha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT hora, producto, cantidad, precio, total
        FROM ventas
        WHERE fecha = ?
        ORDER BY id DESC
    """, (fecha,))
    datos = cursor.fetchall()
    conn.close()
    return datos


def obtener_ventas_por_fecha(fecha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT hora, producto, cantidad, precio, total
        FROM ventas
        WHERE fecha = ?
        ORDER BY id DESC
    """, (fecha,))
    datos = cursor.fetchall()
    conn.close()
    return datos


def total_del_dia(fecha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT SUM(total) FROM ventas WHERE fecha = ?",
        (fecha,)
    )
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado if resultado else 0


def total_por_fecha(fecha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT SUM(total) FROM ventas WHERE fecha = ?",
        (fecha,)
    )
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado if resultado else 0

def insertar_gasto(fecha, hora, descripcion, monto):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO gastos (fecha, hora, descripcion, monto)
        VALUES (?, ?, ?, ?)
    """, (fecha, hora, descripcion, monto))
    conn.commit()
    conn.close()


def obtener_gastos_por_fecha(fecha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT hora, descripcion, monto
        FROM gastos
        WHERE fecha = ?
        ORDER BY id DESC
    """, (fecha,))
    datos = cursor.fetchall()
    conn.close()
    return datos


def total_gastos_por_fecha(fecha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(monto) FROM gastos WHERE fecha = ?", (fecha,))
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado if resultado else 0

def obtener_ventas_en_rango(fecha_inicio, fecha_fin):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT fecha, SUM(total)
        FROM ventas
        WHERE fecha BETWEEN ? AND ?
        GROUP BY fecha
        ORDER BY fecha ASC
    """, (fecha_inicio, fecha_fin))
    datos = cursor.fetchall()
    conn.close()
    return datos


def obtener_gastos_en_rango(fecha_inicio, fecha_fin):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT fecha, SUM(monto)
        FROM gastos
        WHERE fecha BETWEEN ? AND ?
        GROUP BY fecha
        ORDER BY fecha ASC
    """, (fecha_inicio, fecha_fin))
    datos = cursor.fetchall()
    conn.close()
    return datos


def total_ventas_en_rango(fecha_inicio, fecha_fin):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(total)
        FROM ventas
        WHERE fecha BETWEEN ? AND ?
    """, (fecha_inicio, fecha_fin))
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado if resultado else 0


def total_gastos_en_rango(fecha_inicio, fecha_fin):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(monto)
        FROM gastos
        WHERE fecha BETWEEN ? AND ?
    """, (fecha_inicio, fecha_fin))
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado if resultado else 0

def crear_usuario_inicial():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    cantidad = cursor.fetchone()[0]

    if cantidad == 0:
        cursor.execute("""
            INSERT INTO usuarios (nombre, username, password, rol)
            VALUES (?, ?, ?, ?)
        """, ("Administrador", "admin", "1234", "admin"))

    conn.commit()
    conn.close()


def validar_usuario(username, password):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nombre, username, rol
        FROM usuarios
        WHERE username = ? AND password = ?
    """, (username, password))

    usuario = cursor.fetchone()
    conn.close()
    return usuario


def obtener_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nombre, username, rol
        FROM usuarios
        ORDER BY id ASC
    """)
    datos = cursor.fetchall()
    conn.close()
    return datos


def insertar_usuario(nombre, username, password, rol):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuarios (nombre, username, password, rol)
        VALUES (?, ?, ?, ?)
    """, (nombre, username, password, rol))
    conn.commit()
    conn.close()