import logging

from flask_restful import Resource
from flask import request
# from app.config import Config

logger = logging.getLogger(__name__)

class Hello(Resource):
	"""docstring for Hello"""
	def get(Resource):
		return "Hello"
