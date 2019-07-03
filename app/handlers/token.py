import logging

from flask_restful import Resource
from flask import request, jsonify
import random
import string
token_pool = []
assign_token = []
# from app.config import Config

logger = logging.getLogger(__name__)

class NewToken(Resource):
	"""docstring for Hello"""
	def get(self):
		# token_pool = []
		global token_pool
		for x in range(5):
			token = self.randomString() 
			token_pool.append(token)
		return jsonify(data=token_pool, status=200)

	def randomString(self, stringlength=10):
		"""Generate a random string of fixed length """
		letters = string.ascii_lowercase
		return ''.join(random.sample(letters,stringlength))


class AssignToken(Resource):
	"""docstring for AssignToken"""
	def get(self):
		global token_pool
		global assign_token
		token = random.choice(token_pool)
		token_pool.remove(token)
		assign_token.append(token)
		print(token_pool)
		print("-----------------------------------------------------------")
		print(assign_token)
		return jsonify(token=token, status=200)
		