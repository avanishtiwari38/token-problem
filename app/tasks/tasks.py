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
def check_five_min(data):
	token = data['token']
	query = Token.query.filter_by(token = token).one_or_none()
	data = TokenSchema().dump(query).data
	current_time = datetime.datetime.now()
	current_time = time.mktime(current_time.timetuple())
	fiveminutes = 5*60
	if data:
		time_diff = current_time - data['updated_on']
		logger.info(time_diff)
		logger.info(fiveminutes)
		if (time_diff >= fiveminutes):
			query = Token.query.filter_by(token = token).one()
			dataDelete = TokenSchema().dump(query).data
			update_query = Token.query.filter_by(token_id = dataDelete['token_id']).update({'deleted':True})
			db.session.commit()

@celery_obj.task(queue='check_one_min')
def check_one_min(data):
	token = data['token']
	query = Token.query.filter_by(token = token).one_or_none()
	data = TokenSchema().dump(query).data
	current_time = datetime.datetime.now()
	current_time = time.mktime(current_time.timetuple())
	oneminutes = 1*60
	if data:
		time_diff = current_time - data['updated_on']
		logger.info(time_diff)
		logger.info(oneminutes)
		if (time_diff >= oneminutes):
			query = Token.query.filter_by(token = token).one()
			dataDelete = TokenSchema().dump(query).data
			update_query = Token.query.filter_by(token_id = dataDelete['token_id']).update({'assigned':False})
			db.session.commit()