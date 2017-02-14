#!/usr/bin/python3 python3
import os
import json
from app import create_app, db

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.models import User,Role,Text,Comment
app = create_app('default')
app.secret_key = 'abcdefghijklmn'
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role,Text=Text,Comment=Comment)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    #manager.run()
