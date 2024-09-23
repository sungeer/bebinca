from flask import request

from viper.models.user_model import UserModel
from viper.utils.tools import jsonify, abort
from viper.utils.log_util import logger
from viper.utils import jwt_util


def index():
    return jsonify()
