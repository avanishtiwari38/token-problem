import logging
import datetime
import time
import random
import string

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import DataError
from marshmallow import ValidationError

from flask_restful import Resource
from flask import request, jsonify

from app.models.token_model import Token, TokenSchema
from app.models import *
from app.tasks.tasks import check_five_min, check_one_min

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
				dataSchema = TokenSchema().load(data).data 
				token_pool.append(token)

				db.session.add(dataSchema)
				db.session.commit()
				db.session.close()

				check_five_min.s(data).apply_async(countdown=5*60)
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
			check_one_min.s(token).apply_async(countdown=60)
			check_five_min.s(token).apply_async(countdown=5*60)
			return jsonify(token=token, status=200)
		except DataError as e:
			logger.exception(str(e))
			return jsonify(status=400, msg="Data error")
		except NoResultFound as e:
			logger.exception(str(e))
			return jsonify(status=400, msg=str(e))
		except Exception as e:
			logger.exception(str(e))
			return jsonify(status=400, msg=str(e))


class UnassignToken(Resource):
	"""docstring for UnassignToken"""
	def post(self):
		try:
			request_data = request.get_json()
			# update_query = Token.query.filter_by(token_id = token['token_id']).update({'assigned':True})
			query = Token.query.filter_by(token = request_data['token']).one_or_none()
			data = TokenSchema().dump(query).data
			if data:
				update_query = Token.query.filter_by(token_id = data['token_id']).update({'assigned':False, 'updated_on':datetime.datetime.now()})
				db.session.commit()
				check_five_min.s(data).apply_async(countdown=5*60)
				return jsonify(token=data, status=200)
			else:
				return jsonify(msg="Token not found or deleted", status = 400)
		except DataError as e:
			logger.exception(str(e))
			return jsonify(status=400, msg="Data error")
		except NoResultFound as e:
			logger.exception(str(e))
			return jsonify(status=400, msg=str(e))
		except Exception as e:
			logger.exception(str(e))
			return jsonify(status=400, msg=str(e))

class DeleteToken(Resource):
	"""docstring for DeleteToken"""
	def post(self):
		try:
			request_data = request.get_json()
			# update_query = Token.query.filter_by(token_id = token['token_id']).update({'assigned':True})
			query = Token.query.filter_by(token = request_data['token']).one_or_none()
			data = TokenSchema().dump(query).data
			if data:
				update_query = Token.query.filter_by(token_id = data['token_id']).update({'deleted':True})
				db.session.commit()
				return jsonify(token=data, status=200)
			else:
				return jsonify(msg="Token not found", status=400)
		except DataError as e:
			logger.exception(str(e))
			return jsonify(status=400, msg="Data error")
		except NoResultFound as e:
			logger.exception(str(e))
			return jsonify(status=400, msg=str(e))
		except Exception as e:
			logger.exception(str(e))
			return jsonify(status=400, msg=str(e))

class RefreshToken(Resource):
	"""docstring for RefreshToken"""
	def post(self):
		try:
			request_data = request.get_json()
			# update_query = Token.query.filter_by(token_id = token['token_id']).update({'assigned':True})
			query = Token.query.filter_by(token = request_data['token'], assigned = True).one_or_none()
			data = TokenSchema().dump(query).data
			if data:
				update_query = Token.query.filter_by(token_id = data['token_id']).update({'updated_on':datetime.datetime.now()})
				db.session.commit()
				check_one_min.s(data).apply_async(countdown=60)
				check_five_min.s(data).apply_async(countdown=5*60)
				return jsonify(token=data, status=200)
			else:
				return jsonify(msg="token is not assigned or deleted", status=400)
		except DataError as e:
			logger.exception(str(e))
			return jsonify(status=400, msg="Data error")
		except NoResultFound as e:
			logger.exception(str(e))
			return jsonify(status=400, msg=str(e))
		except Exception as e:
			logger.exception(str(e))
			return jsonify(status=400, msg=str(e))