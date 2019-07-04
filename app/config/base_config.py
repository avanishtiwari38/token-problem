
class BaseConfig:
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    CELERY_TIMEZONE = 'Asia/Calcutta'

    # Reuslt backend changed to amqp to use result expires feature. Not very well aware of other amqp vs rpc benefits.
    result_backend = 'amqp://'
    task_default_queue = 'default'
    celery_task_routes = {
    						'tasks.tasks.check_five_min': {'queue': 'check_five_min'},
    						'tasks.tasks.check_one_min': {'queue': 'check_one_min'},
    					}

    task_queues = {
    	'default': {
    		"exchange": "default",
    		"binding_key": "default",
    	},
    	'check_five_min': {
    		'exchange': 'check_five_min',
    		'routing_key': 'check_five_min',
    	},
    	'check_one_min': {
    		'exchange': 'check_one_min',
    		'routing_key': 'check_one_min',
    	},
    }