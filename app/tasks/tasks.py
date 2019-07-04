import os
import logging
import datetime
import time
import copy

from sqlalchemy.orm.exc import NoResultFound
from app import celery_obj
from app.models.token_model import Token, TokenSchema
from app import db

logger = logging.getLogger(__name__)


@celery_obj.task(queue='check_five_min')
def check_five_min():
	# token = data['token']
	token = 'gwzxphnoif'
	print("celery task")
	query = Token.query.filter_by(token = token).one()
	data = TokenSchema().dump(query).data
	current_time = datetime.datetime.now()
	time_diff = current_time - data['updated_on']
	print(time_diff)
	# from_date = int(self.request.args.get('from_date', time.mktime((datetime.datetime.now() - datetime.timedelta(days=7)).timetuple())))

@celery_obj.task(queue='check_one_min')
def check_one_min(data):
	pass
