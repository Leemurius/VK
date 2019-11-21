#!/usr/bin/python3
import sys
sys.path.insert(0, '/var/www/messenger/')

activate_this = '/var/www/messenger/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from app import create_app
application=create_app()
