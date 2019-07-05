from .base_config import BaseConfig


class Config(BaseConfig):
    LOG_PATH = '/var/www/html/token_problem/token_problem/token_problem-app.log'

    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:root@localhost/token_problem"
    FLASK_DEBUG = True
    FLASK_ENV = "development"

    RABBITMQ_HOST = 'localhost'
    RABBITMQ_PORT = 5672
    RABBITMQ_USER = 'guest'
    RABBITMQ_PASSWORD = 'guest'
    broker_url = 'amqp://localhost//'
    # broker_url = "amqp://{}:{}@{}:{}//".format(RABBITMQ_USER, RABBITMQ_PASSWORD, RABBITMQ_HOST, RABBITMQ_PORT)