import logging

from flask_restful import Resource
from flask import request
from app.tasks.tasks import check_five_min, check_one_min
# from app.config import Config

logger = logging.getLogger(__name__)

class Hello(Resource):
	"""docstring for Hello"""
	def get(self):
		task = check_five_min.delay()
		# check_one_min.delay()
		print(task.state)
		return "Hello"
