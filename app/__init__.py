from flask import Flask, Blueprint
from flask_restplus import Api

from .config import Config
from app.rest import api
from app.front import routes
from .database import db
from flask_sqlalchemy import SQLAlchemy

from redis import Redis
import rq

def create_app():
    app = Flask(__name__)

    # Config
    app.config.from_object(Config)

    # Separate API module
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)

    app.register_blueprint(blueprint)

    # Frontend
    app.register_blueprint(routes)

    # DB
    db.init_app(app)

    # redis
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('training-tasks', connection=app.redis)

    return app
