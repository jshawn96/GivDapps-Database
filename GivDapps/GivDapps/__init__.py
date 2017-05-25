from flask import Flask, render_template
from flask_sqlalchemy import sqlalchemy
from flask_migrate import migrate, MigrateCommand
from flask_script import Manager

app = Flask(__name__)
app.config.from_object('GivDapps.default_settings')
manager = Manager(app)

db = sqlalchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

from GivDapps.models import *

@app.route("/")
def hello():
    return render_template("index.html")
