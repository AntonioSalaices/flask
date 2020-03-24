from wtforms import Form
from wtforms import StringField, TextField, PasswordField, HiddenField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms import validators

def length_honeypot(form, field):
   if len(field.data)>0:
       raise validators.ValidationError("El campo debe de estar vacío")

class CommentForm(Form):
    username = StringField('username', 
    [
        validators.Required(message="El username es requerido."),
        validators.length(min=4, max=25, message="Ingrese un username válido")
    ])
    email = EmailField('Correo electronico', 
    [
        validators.Required(message="El username es requerido."),
        validators.Email(message="Ingrese un email válido")
    ]
    )
    comment = TextField('Comentario', [validators.length(min=4, max=25, message="Ingrese un username válido")])
    honeypot = TextField('',[length_honeypot])

class LoginForm(Form):
    username= StringField('username',
    [
        validators.Required(message="El username es requerido."),
        validators.length(min=4, max=25, message="Ingrese un username válido")
    ]
    )
    password = PasswordField('Correo electronico', 
    [
        validators.Required(message="El username es requerido."),
    ]
    )

class CreateForm(Form):
    username= TextField('username',
    [
        validators.Required(message="El username es requerido."),
        validators.length(min=4, max=50, message="Ingrese un username válido")
    ]
    )
    password = PasswordField('password', 
    [
        validators.Required(message="El password es requerido."),
    ]
    )
    email= EmailField('email',
    [
        validators.Required(message="El email es requerido."),
        validators.length(min=4, max=50, message="Ingrese un email válido")
    ]
    )
    submit = SubmitField('submit')