import os
import logging
import datetime
import time
import copy
# from datetime import datetime, time


from sqlalchemy.orm.exc import NoResultFound
from app import celery_obj
from app.models.token_model import Token, TokenSchema
from app import db

logger = logging.getLogger(__name__)


@celery_obj.task(queue='check_five_min')
def check_five_min():
	# token = data['token']
	token = 'gwzxphnoif'
	query = Token.query.filter_by(token = token).one()
	data = TokenSchema().dump(query).data
	current_time = datetime.datetime.now()
	current_time = time.mktime(current_time.timetuple())
	time_diff = current_time - data['updated_on']
	fiveminutes = 5*60*1000
	logger.info(fiveminutes)
	if (time_diff >= fiveminutes):
		query = Token.query.filter_by(token = request_data['token']).one()
		data = TokenSchema().dump(query).data
		update_query = Token.query.filter_by(token_id = data['token_id']).update({'deleted':True})
		db.session.commit()

@celery_obj.task(queue='check_one_min')
def check_one_min():
	token = 'gwzxphnoif'
	query = Token.query.filter_by(token = token).one()
	data = TokenSchema().dump(query).data
	current_time = datetime.datetime.now()
	current_time = time.mktime(current_time.timetuple())
	time_diff = current_time - data['updated_on']
