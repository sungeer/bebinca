from flask import request, render_template

from viper.models.user_model import UserModel
from viper.utils.tools import jsonify, abort
from viper.utils import jwt_util


def index():
    return render_template('chat/index.html')
