from flask import Flask
from flask import render_template
import forms
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask_wtf import CSRFProtect
from flask import make_response
from flask import flash
from flask import json
from flask import g
from config import DevelopmentConfig
from models import db, User, Comment
from helper import date_format
from flask_mail import Mail
from flask_mail import Message
import threading
from flask import copy_current_request_context

app = Flask(__name__)


app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()
mail = Mail()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# @app.route('/ajax-login', methods=['POST'])
# def ajax_login():
#     username = request.form['username']
#     response = {'status':200,'username': username, 'id':1}
#     return json.dumps(response)

@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['comment']:
        return redirect(url_for('login'))
    elif 'username' in session and request.endpoint in ['login', 'create']:
        return redirect(url_for('index'))

def send_email(user_email, username):
    msg = Message('Gracias por tu registro.', sender= app.config['MAIL_USERNAME'],recipients=[user_email] )
    with app.app_context():
        msg.html = render_template('email.html', user= username)
        mail.send(msg)

    


@app.after_request
def after_request(response):
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        username = session['username']
        print(username)
    titulo= "Index"
    return render_template('index.html', titulo=titulo)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
     if 'username' in session:
         session.pop('username')
     return redirect(url_for('login'))

@app.route('/create',methods=['GET', 'POST'])
def create():
    titulo= "Crear Usuario"
    create_form = forms.CreateForm(request.form)
    
    if request.method=="POST" and create_form.validate():
        user = User(create_form.username.data, create_form.password.data, create_form.email.data)
        db.session.add(user)
        db.session.commit()
        @copy_current_request_context
        def send_message(email, username):
            send_email(email, username)


        sender = threading.Thread(name="mail_sender", target=send_email,args= (user.email, user.username))
        sender.start()
        success_message ='Usuario registrado'
        flash(success_message)
    return render_template('create.html', form=create_form, titulo=titulo)


@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Entre")
    titulo= "Login seguro"
    login_form = forms.LoginForm(request.form)
    if request.method=="POST":
        print("Entre POST")
        username = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(username=username).first()
        print(user)
        if user is not None and user.verify_password(password):
            success_message ='Bienvenido {}'.format(username)
            flash(success_message)
            session['username'] = username
            session['user_id'] = user.id

            return redirect(url_for('index'))
        else:
            error_message = 'Usuario o contraseña no válida'
            flash(error_message)
        session['username'] = login_form.username.data
    return render_template('login.html', form=login_form, titulo=titulo)

@app.route('/cookie', methods=['GET', 'POST'])
def cookie():
    response= make_response(render_template('cookie.html'))
    response.set_cookie('custome_cookie', 'Antonio')
    return response

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    titulo= "Crear Comentario"
    comment_form = forms.CommentForm(request.form)
    if request.method=="POST" and comment_form.validate():
        user_id = session['user_id']
        comment = Comment(user_id= user_id, text= comment_form.comment.data)
        db.session.add(comment)
        db.session.commit()
        success_message ='Nuevo comentario creados'
        flash(success_message)
    return render_template('comment.html', form=comment_form, titulo=titulo)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     comment_form = forms.CommentForm(request.form)
#     if request.method=="POST" and comment_form.validate():
#         print(comment_form.username.data)
#         print(comment_form.email.data)
#         print(comment_form.comment.data)
#     else:
#         print("Error en el formulario")
#     titulo="Curso de Flask"
#     return render_template('index.html', titulo=titulo, form= comment_form)

@app.route('/cliente')
def cliente():
    lista=['Antonio', 'Daniela', 'Danna','Sofía']
    return render_template('cliente.html', lista=lista)
    
@app.route('/reviews', methods=['GET'])
@app.route('/reviews/<int:page>', methods=['GET'])
def reviews(page=1):
    per_page=3
    comment_list = Comment.query.join(User).add_columns(User.username, Comment.text, Comment.created_date).paginate(page,per_page,False)
    return render_template('reviews.html', comment_list=comment_list, date_format=date_format)
    
if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=8000)