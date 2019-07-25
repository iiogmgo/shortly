import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# config
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'shortly.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'shortlyisgood'

# db
db = SQLAlchemy(app)

# routes
from shortly import routes
app.register_blueprint(routes.bp)
app.add_url_rule('/', endpoint='index')
