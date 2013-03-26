# -*- coding: UTF-8 -*-
import psycopg2 as pgsql
import sys

def connection(args=None): 
    if args is None:
        from Load.loadconfig import load
       
        args = {}
        
        args['dbname'] = load('DATABASE', 'DBNAME')
        args['user'] = load('DATABASE', 'USER')
        args['host'] = load('DATABASE', 'HOST')
        args['password'] = load('DATABASE', 'PASSWORD')

        args = " ".join(["%s=\'%s\'" % (k, v) for k, v in args.items()])
    # Conexión a la base de datos: 
    try:
        conn = pgsql.connect(args)
    except pgsql.OperationalError, e:
        print >> sys.stderr, "\nNo se pudo poner en marcha la base de datos.\n"
        print >> sys.stderr, e
        print >> sys.stdout, 'Error: Revisar el archivo de error.log'
        sys.exit(1)

    # Retornamos la conexión
    return conn

class PgSQL():
    """
    from DB.pgSQL import PgSQL
    db = PgSQL()
    cursor=db.cursor
    cursor.execute("select version()")
    try:
        return cursor.fetchone()[0]
    finally:
        db.connection.commit()
    """
    connection = None
    cursor = None

    def __init__(self):
        # Connect to an existing database
        self.connection = connection()
        self.cursor = self.connection.cursor()

    def __del__(self):
        if self.cursor is not None:
            self.cursor.close();

        if self.connection is not None:
            self.connection.close();