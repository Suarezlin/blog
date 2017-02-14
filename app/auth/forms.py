from flask_wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email,EqualTo,ValidationError
from ..models import User

class LoginForm(Form):
    email=StringField('邮箱',validators=[Required(),Length(1,64),Email()])
    password=PasswordField('密码',validators=[Required()])
    remember_me=BooleanField('保持登录')
    submit=SubmitField('登录')
class SignForm(Form):
    name=StringField('姓名',validators=[Required()])
    email=StringField('邮箱',validators=[Required(),Length(1,64),Email()])
    netid=StringField('学号',validators=[Required(),Length(10)])
    password=PasswordField('密码',validators=[Required(),EqualTo('password2',message='两次输入的密码必须相同!')])
    password2=PasswordField('确认密码',validators=[Required()])
    submit=SubmitField('注册')
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱地址已被注册!')
    def validate_netid(self,field):
        if User.query.filter_by(netid=field.data).first():
            raise ValidationError('该学号已被注册!')