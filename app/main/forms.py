from flask_wtf import Form
from wtforms import StringField,SubmitField,PasswordField,TextAreaField,ValidationError
from wtforms.validators import Required,Length,Email,EqualTo
from ..models import User

class signup_form(Form):
    email=StringField('邮箱',validators=[Required(),Length(1,64),Email()])
    username=StringField('昵称',validators=[Required(),Length(1,64)])
    password=PasswordField('密码',validators=[Required(),EqualTo('password2',message='两次输入的密码必须相同!')])
    password2=PasswordField('确认密码',validators=[Required()])
    submit=StringField('注册')
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱地址已被注册!')