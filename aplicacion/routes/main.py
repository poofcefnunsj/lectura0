from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from aplicacion.extensions import db
from aplicacion.models import Usuario, Comentario

main = Blueprint('main', __name__)

#from models import db
#from models import Usuario, Comentario
@main.route('/')
def inicio():
	return render_template('inicio.html')

@main.route('/nuevo_comentario', methods = ['GET','POST'])
def nuevo_comentario():
    if request.method == 'POST':
        if  not request.form['email'] or not request.form['password']:
            return render_template('error.html', error="Por favor ingrese los datos requeridos")
        else:
            usuario_actual= Usuario.query.filter_by(correo= request.form['email']).first()
            if usuario_actual is None:
                return render_template('error.html', error="El correo no está registrado")
            else:
                verificacion = check_password_hash(usuario_actual.clave, request.form['password'])
                if (verificacion):
                    return render_template('ingresar_comentario.html', usuario = usuario_actual)
                else:
                    return render_template('error.html', error="La contraseña no es válida")
    else:
        return render_template('nuevo_comentario.html')


@main.route('/ingresar_comentario', methods = ['GET', 'POST'])
def ingresar_comentario():
    if request.method == 'POST':
        if not request.form['contenido']:
            return render_template('error.html', error="Contenido no ingresado...")
        else:
            nuevo_comentario= Comentario(fecha=datetime.now(), contenido=request.form['contenido'], usuario_id =request.form['userId'])
            db.session.add(nuevo_comentario)
            db.session.commit()
            return render_template('inicio.html')
    return render_template('inicio.html')

@main.route('/listar_comentarios')
def listar_comentarios():
   return render_template('listar_comentario.html', comentarios = Comentario.query.all())

@main.route('/listar_comentarios_usuario', methods = ['GET', 'POST'])
def listar_comentarios_usuario():
    if request.method == 'POST':
        if not request.form['usuarios']:
			#Pasa como parámetro todos los usuarios
            return render_template('listar_comentario_usuario.html', usuarios = Usuario.query.all(), usuario_seleccionado = None )
        else:
            return render_template('listar_comentario_usuario.html', usuarios= None, usuario_selec = Usuario.query.get(request.form['usuarios']))
    else:
        return render_template('listar_comentario_usuario.html', usuarios = Usuario.query.all(), usuario_selec = None )
