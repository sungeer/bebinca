from flask import request

from bebinca.models.user_model import UserModel
from bebinca.utils.tools import jsonify, abort
from bebinca.utils.log_util import logger
from bebinca.utils import jwt_util


def index():
    return jsonify()
