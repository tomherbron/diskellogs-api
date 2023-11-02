from flask import Blueprint, jsonify

from api import token_required

views = Blueprint('views', __name__)


@views.route('/home', methods=['GET', 'POST'])
@token_required
def home():
    return jsonify('Ok!!!')

