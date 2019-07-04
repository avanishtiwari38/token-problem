import logging

from flask_restful import Resource
from flask import request
from app.tasks.tasks import check_five_min
# from app.config import Config

logger = logging.getLogger(__name__)

class Hello(Resource):
	"""docstring for Hello"""
	def get(self):
		check_five_min.delay()
		return "Hello"
