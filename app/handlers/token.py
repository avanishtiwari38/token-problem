import logging
import datetime
import time

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import DataError
from marshmallow import ValidationError

from flask_restful import Resource
from flask import request, jsonify
import random
import string
from app.models.token_model import Token, TokenSchema
from app.models import *
# from app.config import Config

logger = logging.getLogger(__name__)

class NewToken(Resource):
	"""docstring for Hello"""
	def get(self):
		try:
			token_pool = []
			for x in range(5):
				token = self.randomString()
				data = {}
				data['token'] = token
				data = TokenSchema().load(data).data 
				token_pool.append(token)

				db.session.add(data)
				db.session.commit()
				db.session.close()
			return jsonify(data=token_pool, status=200)
		except Exception as e:
			raise e

	def randomString(self, stringlength=10):
		"""Generate a random string of fixed length """
		letters = string.ascii_lowercase
		return ''.join(random.sample(letters,stringlength))


class AssignToken(Resource):
	"""docstring for AssignToken"""
	def get(self):
		try:
			query = Token.query.filter_by(assigned=False, deleted=False)
			data = TokenSchema(many=True).dump(query.all()).data
			token = random.choice(data)
			update_query = Token.query.filter_by(token_id = token['token_id']).update({'assigned':True, 'updated_on':datetime.datetime.now()})
			db.session.commit()
			return jsonify(token=token, status=200)
		except DataError as e:
			logger.exception(str(e))
			return self.return_json(status=400, msg="Data error")
		except NoResultFound as e:
			logger.exception(str(e))
			return self.return_json(status=400, msg=str(e))
		except Exception as e:
			logger.exception(str(e))
			return self.return_json(status=400, msg=str(e))


class UnassignToken(Resource):
	"""docstring for UnassignToken"""
	def post(self):
		try:
			request_data = request.get_json()
			# update_query = Token.query.filter_by(token_id = token['token_id']).update({'assigned':True})
			query = Token.query.filter_by(token = request_data['token']).one()
			data = TokenSchema().dump(query).data
			update_query = Token.query.filter_by(token_id = data['token_id']).update({'assigned':False, 'updated_on':datetime.datetime.now()})
			db.session.commit()
			return jsonify(token=data, status=200)
		except DataError as e:
			logger.exception(str(e))
			return self.return_json(status=400, msg="Data error")
		except NoResultFound as e:
			logger.exception(str(e))
			return self.return_json(status=400, msg=str(e))
		except Exception as e:
			logger.exception(str(e))
			return self.return_json(status=400, msg=str(e))

class DeleteToken(Resource):
	"""docstring for DeleteToken"""
	def post(self):
		try:
			request_data = request.get_json()
			# update_query = Token.query.filter_by(token_id = token['token_id']).update({'assigned':True})
			query = Token.query.filter_by(token = request_data['token']).one()
			data = TokenSchema().dump(query).data
			update_query = Token.query.filter_by(token_id = data['token_id']).update({'deleted':True})
			db.session.commit()
			return jsonify(token=data, status=200)
		except DataError as e:
			logger.exception(str(e))
			return self.return_json(status=400, msg="Data error")
		except NoResultFound as e:
			logger.exception(str(e))
			return self.return_json(status=400, msg=str(e))
		except Exception as e:
			logger.exception(str(e))
			return self.return_json(status=400, msg=str(e))

class RefreshToken(Resource):
	"""docstring for RefreshToken"""
	def post(self):
		try:
			request_data = request.get_json()
			# update_query = Token.query.filter_by(token_id = token['token_id']).update({'assigned':True})
			query = Token.query.filter_by(token = request_data['token']).one()
			data = TokenSchema().dump(query).data
			update_query = Token.query.filter_by(token_id = data['token_id']).update({'updated_on':datetime.datetime.now()})
			db.session.commit()
			return jsonify(token=data, status=200)
		except DataError as e:
			logger.exception(str(e))
			return self.return_json(status=400, msg="Data error")
		except NoResultFound as e:
			logger.exception(str(e))
			return self.return_json(status=400, msg=str(e))
		except Exception as e:
			logger.exception(str(e))
			return self.return_json(status=400, msg=str(e))