from DB.pgSQL import PgSQL




class user():
    def useradd(self,a,b):
        db = PgSQL()
        cursor=db.cursor
        cursor.execute("select version()")
        try:
            return cursor.fetchone()
        finally:
            db.connection.commit()
    
    def buscaruser(self,user=None,dni=None,imei=None,telefono=None,email=None):
        db = PgSQL() #conectar a la base de datos
        cursor=db.cursor #Crear el conector
        
        sql="""select tx_numero,tx.tx_id
                from vehiculo vh 
                inner join taxi tx on vh.vh_id=tx.vh_id
                inner join taxista_rol_taxi trt on trt.tx_id=tx.tx_id
                inner join taxista txt on trt.txt_id=txt.txt_id
                where TRUE=TRUE
            """
        if user is not None:
            #sql = sql+" AND user=%s" % (int(user))
            pass
        if dni is not None:
            sql = sql + " AND txt.txt_dni = '%s'" % (dni)
        if imei is not None:
            sql = sql + " AND vh.vh_imei = '%s'" % (imei)
        if telefono is not None:
            sql = sql + " AND (txt.txt_telefono1 = '%s' OR txt.txt_telefono1 = '%s' )" % (telefono,telefono)
        if email is not None:
            pass
            #sql = sql + " AND email='%s'" % (email)
        sql=sql+" order by txt.txt_nombre"
            
        cursor.execute(sql) #Hacer la consulta
        try:
            return cursor.fetchall() #devolver el resultado
        finally:
            db.connection.commit()