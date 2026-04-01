import pandas as pd
import mysql.connector


class GestionBBDD:
    """
    Clase para gestionar operaciones básicas sobre una base de datos MySQL.

    Permite:
    - Crear bases de datos o tablas
    - Insertar uno o varios registros
    - Ejecutar consultas que devuelvan un DataFrame
    - Ejecutar consultas que devuelvan una lista de tuplas

    Atributos:
    ----------
    user : str
        Usuario de MySQL.
    password : str
        Contraseña de MySQL.
    host : str
        Dirección del servidor de MySQL.
    """

    def __init__(self, password, user="root", host="127.0.0.1"):
        """
        Inicializa los parámetros de conexión a MySQL.

        Parámetros:
        ----------
        password : str
            Contraseña de MySQL.
        user : str, default="root"
            Usuario de MySQL.
        host : str, default="127.0.0.1"
            Host del servidor de MySQL.
        """
        self.user = user
        self.password = password
        self.host = host

    def crear_conexion(self, nombre_bbdd=None):
        """
        Crea y devuelve una conexión a MySQL.

        Parámetros:
        ----------
        nombre_bbdd : str, default=None
            Nombre de la base de datos a la que se quiere conectar.
            Si es None, la conexión se realiza sin seleccionar base de datos.

        Returns:
        -------
        mysql.connector.connection.MySQLConnection
            Objeto de conexión a MySQL.
        """
        if nombre_bbdd is None:
            conexion = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host
            )
        else:
            conexion = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                database=nombre_bbdd
            )

        return conexion

    def ejecutar_ddl(self, query, nombre_bbdd=None):
        """
        Ejecuta una consulta SQL de definición de estructura, como CREATE DATABASE,
        CREATE TABLE, ALTER TABLE o DROP TABLE.

        Parámetros:
        ----------
        query : str
            Consulta SQL a ejecutar.
        nombre_bbdd : str, default=None
            Nombre de la base de datos sobre la que se ejecuta la consulta.
            Si es None, se conecta sin base de datos seleccionada.

        Returns:
        -------
        None
        """
        conexion = self._crear_conexion(nombre_bbdd)
        cursor = conexion.cursor()

        try:
            cursor.execute(query)
            print("Consulta ejecutada correctamente.")

        except mysql.connector.Error as error:
            print(error)
            print("Error Code:", error.errno)
            print("SQLSTATE:", error.sqlstate)
            print("Message:", error.msg)

        finally:
            cursor.close()
            conexion.close()

    def insertar_dato(self, query, nombre_bbdd, datos):
        """
        Inserta un único registro en una tabla.

        Parámetros:
        ----------
        query : str
            Consulta SQL de inserción con placeholders.
            Ejemplo: INSERT INTO tabla (col1, col2) VALUES (%s, %s)
        nombre_bbdd : str
            Nombre de la base de datos.
        datos : tuple
            Tupla con los valores que se van a insertar.

        Returns:
        -------
        None
        """
        conexion = self._crear_conexion(nombre_bbdd)
        cursor = conexion.cursor()

        try:
            cursor.execute(query, datos)
            conexion.commit()
            print(cursor.rowcount, "registro/s insertado/s.")

        except mysql.connector.Error as error:
            print(error)
            print("Error Code:", error.errno)
            print("SQLSTATE:", error.sqlstate)
            print("Message:", error.msg)

        finally:
            cursor.close()
            conexion.close()

    def insertar_datos(self, query, nombre_bbdd, lista_datos):
        """
        Inserta múltiples registros en una tabla usando una lista de tuplas.

        Parámetros:
        ----------
        query : str
            Consulta SQL de inserción con placeholders.
            Ejemplo: INSERT INTO tabla (col1, col2) VALUES (%s, %s)
        nombre_bbdd : str
            Nombre de la base de datos.
        lista_datos : list[tuple]
            Lista de tuplas con los valores que se van a insertar.

        Returns:
        -------
        None
        """
        conexion = self._crear_conexion(nombre_bbdd)
        cursor = conexion.cursor()

        try:
            cursor.executemany(query, lista_datos)
            conexion.commit()
            print(cursor.rowcount, "registro/s insertado/s.")

        except mysql.connector.Error as error:
            print(error)
            print("Error Code:", error.errno)
            print("SQLSTATE:", error.sqlstate)
            print("Message:", error.msg)

        finally:
            cursor.close()
            conexion.close()

    def consultar_dataframe(self, query, nombre_bbdd):
        """
        Ejecuta una consulta SQL y devuelve el resultado en un DataFrame.

        Parámetros:
        ----------
        query : str
            Consulta SQL de tipo SELECT.
        nombre_bbdd : str
            Nombre de la base de datos.

        Returns:
        -------
        pandas.DataFrame
            DataFrame con los resultados de la consulta.
        """
        conexion = self._crear_conexion(nombre_bbdd)

        try:
            dataframe_resultado = pd.read_sql(query, conexion)
            return dataframe_resultado

        except mysql.connector.Error as error:
            print(error)
            print("Error Code:", error.errno)
            print("SQLSTATE:", error.sqlstate)
            print("Message:", error.msg)

        finally:
            conexion.close()

    def consultar_tuplas(self, query, nombre_bbdd):
        """
        Ejecuta una consulta SQL y devuelve el resultado como una lista de tuplas.

        Parámetros:
        ----------
        query : str
            Consulta SQL de tipo SELECT.
        nombre_bbdd : str
            Nombre de la base de datos.

        Returns:
        -------
        list[tuple]
            Lista de tuplas con los resultados de la consulta.
        """
        conexion = self._crear_conexion(nombre_bbdd)
        cursor = conexion.cursor()

        try:
            cursor.execute(query)
            resultados = cursor.fetchall()
            return resultados

        except mysql.connector.Error as error:
            print(error)
            print("Error Code:", error.errno)
            print("SQLSTATE:", error.sqlstate)
            print("Message:", error.msg)

        finally:
            cursor.close()
            conexion.close()