
import logging
import traceback

from flask_restplus import Api

import app.config
from sqlalchemy.orm.exc import NoResultFound

from .models.controller import api as models_namespace

log = logging.getLogger(__name__)

# building the API
api = Api(version='1.0', title='Trainer API',
          description='Model Trainer')

api.add_namespace(models_namespace)


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not config.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404