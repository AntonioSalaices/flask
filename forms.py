from wtforms import Form
from wtforms import StringField, TextField, PasswordField, HiddenField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from models import User

# def length_honeypot(form, field):
#    if len(field.data)>0:
#        raise validators.ValidationError("El campo debe de estar vacío")

class CommentForm(Form):
    # username = StringField('username', 
    # [
    #     validators.Required(message="El username es requerido."),
    #     validators.length(min=4, max=25, message="Ingrese un username válido")
    # ])
    # email = EmailField('Correo electronico', 
    # [
    #     validators.Required(message="El username es requerido."),
    #     validators.Email(message="Ingrese un email válido")
    # ]
    # )
    comment = TextField('Comentario', [validators.length(min=4, max=200, message="Ingrese un comentario válido")])
    # honeypot = TextField('',[length_honeypot])
    submit = SubmitField('submit')
class LoginForm(Form):
    username= TextField('username',
    [
        validators.Required(message="El username es requerido."),
        validators.length(min=4, max=50, message="Ingrese un username válido")
    ]
    )
    password = PasswordField('Password', 
    [
        validators.Required(message="El password es requerido."),
    ]
    )
    submit = SubmitField('submit')

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

    def validate_username(form, field):
        username = field.data
        user = User.query.filter_by(username=username).first()
        if user is not None:
            raise validators.ValidationError('El username ya se encuentra registrado')
