
import os
from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_restplus import Api

#############################################

# ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# ########### flask obj #####################

# Serving Flask app "mymain"

app = Flask(__name__)  # __name__ Flask uses the import name to know where to look up resources, templates, static files
api = Api()

# ############ config db , setup db ####################

app.config.from_object(Config)

db = MongoEngine()  #
db.init_app(app)

# ############### API #######################
api.init_app(app)

# views (routes)
from . import routes  # not write it at top of file because it causes import errors