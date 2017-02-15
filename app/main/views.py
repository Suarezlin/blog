from flask import render_template, session, redirect, url_for, flash, request, copy_current_request_context, jsonify, \
    abort, make_response
from . import main
import os
from ..models import User, Text, Follow, Message
from .. import db
from flask_login import login_required, current_user
import time
import datetime
import random


@main.route('/')
@login_required
def index():
    user = current_user
    posts = user.texts.order_by(Text.timestamp.desc()).all()
    leng = len(posts)
    timestamp = []
    for post in posts:
        timestamp.append(utc2local(post.timestamp).strftime('%Y-%m-%d'))
    return render_template('index.html', user=current_user, posts=posts, len=leng, timestamp=timestamp)


@main.route('/user/<email>')
@login_required
def user(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        abort(404)
    if email == current_user.email:
        return render_template('user.html', user=user)
    else:
        return render_template('other.html', user=user)


@main.route('/secret')
@login_required
def secret():
    return '<h1>hello world</h1>'


@main.route('/write')
@login_required
def write():
    return render_template('write.html', user=current_user)


@main.route('/write_blog', methods=['POST'])
@login_required
def write_blog():
    user = current_user
    title = request.form.get('title', None)
    body = request.form.get('body', None)
    txt = request.form.get('txt', None)
    blog = Text(title=title, body=body, author=current_user._get_current_object(), txt=txt)
    db.session.add(blog)
    db.session.commit()
    return jsonify(result='success', id=blog.id)


@main.route('/blog/<id>')
@login_required
def get_blog(id):
    blog = Text.query.filter_by(id=id).first()
    if current_user == blog.author:
        if blog is None:
            abort(404)
        else:
            author = blog.author
            timestamp = utc2local(blog.timestamp).strftime('%Y-%m-%d')
            return render_template('blog.html', author=author, blog=blog, timestamp=timestamp)
    else:
        if blog is None:
            abort(404)
        else:
            author = blog.author
            timestamp = utc2local(blog.timestamp).strftime('%Y-%m-%d')
            return render_template('otherblog.html', author=author, blog=blog, timestamp=timestamp)


@main.route('/delete', methods=['POST'])
@login_required
def delete():
    id = request.form.get('id', None)
    blog = Text.query.filter_by(id=id).first()
    db.session.delete(blog)
    db.session.commit()
    return jsonify(result='success')


@main.route('/edit/<id>')
@login_required
def edit(id):
    blog = Text.query.filter_by(id=id).first()
    if blog is None:
        abort(404)
    else:
        timestamp = utc2local(blog.timestamp).strftime('%Y-%m-%d')
        return render_template('edit.html', blog=blog, user=current_user, timestamp=timestamp)


@main.route('/edit_blog', methods=['POST'])
@login_required
def edit_blog():
    id = request.form.get('id', None)
    title = request.form.get('title', None)
    body = request.form.get('body', None)
    blog = Text.query.filter_by(id=id).first()
    txt = request.form.get('txt', None)
    if current_user.id != blog.author.id:
        abort(403)
    if blog is None:
        abort(404)
    else:
        blog.title = title
        blog.body = body
        blog.txt = txt
        db.session.add(blog)
        db.session.commit()
        return jsonify(result='success')


@main.route('/upload', methods=['POST'])
@login_required
def upload():
    user = current_user
    name = request.form.get('name', None)
    address = request.form.get('address', None)
    about_me = request.form.get('about_me', None)
    if name != '':
        user.name = name
    if address != '':
        user.location = address
    if about_me != '':
        user.about_me = about_me

    db.session.add(user)
    db.session.commit()
    return jsonify(result='success')


@main.route('/upload_avatar', methods=['POST'])
@login_required
def ava():
    user = current_user
    avatar = request.files['avatar']
    fname = avatar.filename
    UPLOAD_FOLDER = os.getcwd() + '/app/static/avatar/'
    if user.real_avatar is not None:
        os.remove(UPLOAD_FOLDER + user.real_avatar)
    avatar.save('{}{}_{}'.format(UPLOAD_FOLDER, current_user.email, fname))
    user.real_avatar = '{}_{}'.format(current_user.email, fname)
    db.session.add(user)
    db.session.commit()
    return jsonify(result='success')


def utc2local(utc_st):
    # “”“UTC时间转本地时间（+8:00）”“”
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st


@main.route('/getinfo', methods=['POST'])
@login_required
def getinfo():
    id = request.form.get('id', None)
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    else:
        if user.real_avatar is not None:
            avatar = '/static/avatar/' + user.real_avatar
        else:
            avatar = user.gravatar()
        time = utc2local(user.member_since).strftime('%Y-%m-%d')
        if current_user.is_following(user):
            following = '1'
        else:
            following = '0'
        followers = len(user.followers.order_by(Follow.timestamp.desc()).all())
        followed = len(user.followed.order_by(Follow.timestamp.desc()).all())
        return jsonify(name=user.name, email=user.email, avatar=avatar, about_me=user.about_me, time=time,
                       address=user.location, following=following, followers=followers, followed=followed)


@main.route('/get_this_blog', methods=['POST'])
@login_required
def get_this_blog():
    id = request.form.get('id', None)
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    else:
        blogs = user.texts.order_by(Text.timestamp.desc()).all()
        time = []
        title = []
        txt = []
        url = []
        id = []
        for blog in blogs:
            title.append(blog.title)
            txt.append(blog.txt)
            time.append(utc2local(blog.timestamp).strftime('%Y-%m-%d'))
            url.append('http://localhost:5000/blog/' + str(blog.id))
            id.append(blog.id)
        return jsonify(title=title, time=time, txt=txt, url=url, id=id)


@main.route('/follow', methods=['POST'])
@login_required
def follow():
    id = request.form.get('id', None)
    method = request.form.get('method', None)
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    if method == 'follow':
        current_user.follow(user)
        message = Message(user=user, sel=current_user.id, do='follow')
        db.session.add(message)
        db.session.commit()
        return jsonify(result='success')
    else:
        current_user.unfollow(user)
        message = Message(user=user, sel=current_user.id, do='unfollow')
        db.session.add(message)
        db.session.commit()
        return jsonify(result='success')


@main.route('/get_following', methods=['POST'])
@login_required
def get_following():
    id = request.form.get('id', None)
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    else:
        following = user.followed.order_by(Follow.timestamp.desc()).all()
        u = []
        for it in following:
            uu = User.query.filter_by(id=it.followed_id).first()
            u.append(uu)
        name = []
        email = []
        text = []
        avatar = []
        blog_num = []
        follower_num = []
        for it in u:
            name.append(it.name)
            email.append(it.email)
            text.append(it.about_me[0:100])
            if it.real_avatar is not None:
                a = 'http://localhost:5000/static/avatar/' + it.real_avatar
            else:
                a = it.gravatar()
            avatar.append(a)
            blog_num.append(len(it.texts.order_by(Text.timestamp.desc()).all()))
            follower_num.append(len(it.followers.order_by(Follow.timestamp.desc()).all()))
        return jsonify(name=name, email=email, intro=text, blog_num=blog_num, follower_num=follower_num, avatar=avatar)


@main.route('/get_follower', methods=['POST'])
@login_required
def get_follower():
    id = request.form.get('id', None)
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    else:
        following = user.followers.order_by(Follow.timestamp.desc()).all()
        u = []
        for it in following:
            uu = User.query.filter_by(id=it.follower_id).first()
            u.append(uu)
        name = []
        email = []
        text = []
        avatar = []
        blog_num = []
        follower_num = []
        for it in u:
            name.append(it.name)
            email.append(it.email)
            text.append(it.about_me[0:100])
            if it.real_avatar is not None:
                a = 'http://localhost:5000/static/avatar/' + it.real_avatar
            else:
                a = it.gravatar()
            avatar.append(a)
            blog_num.append(len(it.texts.order_by(Text.timestamp.desc()).all()))
            follower_num.append(len(it.followers.order_by(Follow.timestamp.desc()).all()))
        return jsonify(name=name, email=email, intro=text, blog_num=blog_num, follower_num=follower_num, avatar=avatar)


@main.route('/discover')
@login_required
def discover():
    return render_template('discover.html')


@main.route('/get_hot_blog', methods=['POST'])
@login_required
def get_hot():
    num = request.form.get('num', None)
    alnum = request.form.get('alnum', None)
    text = Text.query.order_by(Text.timestamp.desc()).all()
    sel_text = text[int(alnum):int(alnum) + int(num)]
    id = []
    title = []
    author = []
    txt = []
    for it in sel_text:
        id.append(it.id)
        title.append(it.title)
        author.append(it.author.name)
        txt.append(it.txt)
    return jsonify(id=id, title=title, author=author, txt=txt)


@main.route('/message')
@login_required
def message():
    return render_template('message.html')


@main.route('/get_message', methods=['POST'])
@login_required
def get_message():
    message = current_user.messages
    new_m = []
    old_m = []
    for it in message:
        u = User.query.filter_by(id=it.sel).first()
        if it.is_read == False:
            if it.do == 'follow':
                new_m.append('<a href=/user/' + u.email + '>' + u.name + '(' + u.email + ')</a> 关注了你')
            else:
                new_m.append('<a href=/user/' + u.email + '>' + u.name + '(' + u.email + ')</a> 取关了你')
        else:
            if it.do == 'follow':
                old_m.append('<a href=/user/' + u.email + '>' + u.name + '(' + u.email + ')</a> 关注了你')
            else:
                old_m.append('<a href=/user/' + u.email + '>' + u.name + '(' + u.email + ')</a> 取关了你')
        it.is_read = True
        db.session.add(it)
    return jsonify(new_m=new_m, old_m=old_m)


@main.route('/get_m_num', methods=['POST'])
@login_required
def get_m_num():
    id = request.form.get('id', None)
    user = User.query.filter_by(id=id).first()
    num = 0
    for it in user.messages:
        if it.is_read == False:
            num = num + 1
    return jsonify(num=num)


@main.route('/test')
def ffff():
    u = User.query.all()
    user = random.choice(u)
    uuu = User.query.filter_by(id=current_user.id).first()
    message = Message(user=uuu, sel=user.id, do='follow')
    f = Follow(follower=user, followed=uuu)
    db.session.add(f)
    db.session.add(message)
    return 'success'


def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))


@main.route('/ckupload/', methods=['POST', 'OPTIONS'])
def ckupload():
    """CKEditor file upload"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")
    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)
        UPLOAD_FOLDER = os.getcwd() + '/app/static/'
        filepath = os.path.join(UPLOAD_FOLDER, 'upload', rnd_name)
        # 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'
        if not error:
            fileobj.save(filepath)
            url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
    else:
        error = 'post error'
    res = """<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>""" % (callback, url, error)
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response
