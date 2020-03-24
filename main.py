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
from models import db, User

app = Flask(__name__)


app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/ajax-login', methods=['POST'])
def ajax_login():
    username = request.form['username']
    response = {'status':200,'username': username, 'id':1}
    return json.dumps(response)

@app.before_request
def before_request():
    g.test = "test"


@app.after_request
def after_request(response):
    print(g.test)
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    print(g.test)
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
    print(create_form.username.data)
    print(create_form.password.data)
    print(create_form.email.data)
    if request.method=="POST" and create_form.validate():
        user = User(username= create_form.username.data, password= create_form.password.data, email=create_form.email.data)
        db.session.add(user)
        db.session.commit()
        success_message ='Usuario registrado en la BD'
        flash(success_message)
    return render_template('create.html', form=create_form, titulo=titulo)


@app.route('/login', methods=['GET', 'POST'])
def login():
    titulo= "Login seguro"
    login_form = forms.LoginForm(request.form)
    if request.method=="POST" and login_form.validate():
        username = login_form.username.data
        success_message ='Bienvenido {}'.format(username)
        flash(success_message)
        session['username'] = login_form.username.data
    return render_template('login.html', form=login_form, titulo=titulo)

@app.route('/cookie', methods=['GET', 'POST'])
def cookie():
    response= make_response(render_template('cookie.html'))
    response.set_cookie('custome_cookie', 'Antonio')
    return response

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    return render_template('comment.html')

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
    
if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=8000)