#todo/app.py
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flaskext.mysql import MySQL #pip install flask-mysql
from flask_restful import Resource, Api
import pymysql


DEBUG=True

app= Flask(__name__)
app.config.from_object(__name__)

mysql=MySQL(app)

app.config['MYSQL_DATABASE_USER'] = 'usuario.suporte'
app.config['MYSQL_DATABASE_PASSWORD'] = 'tp.so'
app.config['MYSQL_DATABASE_DB'] = 'CALLCENTER_DB'
app.config['MYSQL_DATABASE_HOST'] = '35.172.134.127'
mysql.init_app(app)


CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/')
def home():
    conn=mysql.connect()
    cursor=conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT * from usuarios order by id_usuarios")
        userslist = cursor.fetchall()
        return jsonify({
            'status': 'success',
            'usuarios': userslist
        })
    
    except Exception as e:
        print (e)
    finally:
        cursor.close()
        conn.close()
    return render_template('index.html')

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json(silent=True)
        id_usuarios=post_data.get('id_usuarios')
        nombre = post_data.get('nombre')
        apellido = post_data.get('apellido')
        correo = post_data.get('correo')
        telefono = post_data.get('telefono')
        id_agentes = post_data.get('id_agentes')
        id_empresas = post_data.get('id_empresas')
        departamento = post_data.get('departamento')
 
        print(nombre)
        print(apellido)

        sql = "INSERT INTO usuarios(id_usuarios,nombre,apellido,correo,telefono,id_agentes,id_empresas,departamento) VALUES(%s, %s, %s,%s,%s,%s,%s,%s)"
        data = (id_usuarios,nombre, apellido, correo,telefono,id_agentes,id_empresas,departamento)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        
        response_object['message'] = "Cliente Registrado Exitosamente"
    return jsonify(response_object)

@app.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    print(id)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuarios = %s", [id])
    row = cursor.fetchone() 
 
    return jsonify({
        'status': 'success',
        'editmember': row
    })

@app.route('/update', methods=['GET', 'POST'])
def update():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json(silent=True)
        edit_id_usuarios = post_data.get('edit_id_usuarios')
        edit_nombre = post_data.get('edit_nombre')
        edit_apellido = post_data.get('edit_apellido')
        edit_correo = post_data.get('edit_correo')
        edit_telefono = post_data.get('edit_telefono')
        edit_id_agentes = post_data.get('edit_id_agentes')
        edit_id_empresas = post_data.get('edit_id_empresas')
        edit_departamento = post_data.get('edit_departamento')
 
        print(edit_nombre)
        print(edit_apellido)
 
        cursor.execute ("UPDATE usuarios SET nombre=%s, apellido=%s, correo=%s, telefono=%s, id_agentes=%s, id_empresas=%s,departamento=%s WHERE id_usuarios=%s",
                        (edit_nombre, edit_apellido, edit_correo,edit_telefono,edit_id_agentes,edit_id_empresas,edit_departamento, edit_id_usuarios))
        conn.commit()
        cursor.close()
 
        response_object['message'] = "Cliente Actualizado Exitosamente"
    return jsonify(response_object)

@app.route('/delete/<string:id>', methods=['GET', 'POST'])
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
   
    response_object = {'status': 'success'}
 
    cursor.execute("DELETE FROM usuarios WHERE id_usuarios = %s", [id])
    conn.commit()
    cursor.close()
    response_object['message'] = "Cliente Eliminado Exitosamente"
    return jsonify(response_object)


if(__name__=='__main__'):
    app.run(host='0.0.0.0',port=5000,debug=True)


