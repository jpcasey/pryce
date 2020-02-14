__all__ = ['pryce_lists_bp', 'pryce_lists']

from flask import Blueprint

pryce_lists_bp = Blueprint('pryce_lists', __name__, url_prefix='/pryce_lists')
