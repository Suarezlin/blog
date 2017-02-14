from flask import render_template, redirect, url_for, request, flash, jsonify
from . import auth
from ..models import User, db
from flask_login import current_user, login_required, login_user,logout_user
from ..email import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('auth/signup.html')


@auth.route('/login_auth', methods=['POST'])
def login_auth():
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    user = User.query.filter_by(email=email).first()
    if user is not None and user.verify_password(password):
        login_user(user)
        return jsonify(result='success')
    elif user is None:
        return jsonify(result='user name error')
    elif not user.verify_password(password):
        return jsonify(result='password error')


@auth.route('/sign_auth', methods=['POST'])
def sign_auth():
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    confirm = request.form.get('confirm', None)
    user = User.query.filter_by(email=email).first()
    if user is not None:
        return jsonify(result='email is already registered')
    if password != confirm:
        return jsonify(result='password is different from confirm')
    u = User(email=email, password=password)
    db.session.add(u)
    db.session.commit()
    # token=u.generate_confirmation_token()
    # send_email(u.email,'确认你的账户','auth/email/confirm',user=u,token=token)
    return jsonify(result='regiser success')

@auth.route('/mail_test')
def mail_test():
    send_email('1031312670@qq.com','test','auth/email/confirm')
    return '<h1>Success</h1>'

@auth.route('/confirm/<token>')
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        return render_template('auth/confirmcom.html')
    else:
        return render_template('auth/unc.html')

@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:5]!='auth.':
        return redirect(url_for('auth.unconfirmed'))
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous:
        return redirect(url_for('auth.login'))
    elif current_user.confirmed:
        return redirect(url_for('main.index'))
    # token = current_user.generate_confirmation_token()
    # send_email(current_user.email, '确认你的账户', 'auth/email/confirm', user=current_user, token=token)
    return render_template('auth/waitconfirm.html',user=current_user)
@auth.route('/confirm',methods=['POST'])
def resend():
    token=current_user.generate_confirmation_token()
    send_email(current_user.email,'确认你的账户','auth/email/confirm',user=current_user,token=token)
    return jsonify(result='success')
@auth.route('/logout',methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify(result='success')
# @auth.route('/waitconfirm')
# def waitconfirm():
#     return render_template('auth/waitconfirm.html')
