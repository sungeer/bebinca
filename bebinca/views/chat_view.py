from flask import request, Blueprint

from bebinca.models.user_model import UserModel
from bebinca.utils.tools import jsonify, abort
from bebinca.utils.log_util import logger
from bebinca.utils import jwt_util

route = Blueprint('chat', __name__)


@route.post('/')
def index():
    return jsonify()
