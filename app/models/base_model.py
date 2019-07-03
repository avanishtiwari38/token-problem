from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy, models_committed
from flask_migrate import Migrate


migrate = Migrate()
ma = Marshmallow()
db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True

    created_on = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    updated_on = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)


# class NotificationStatus(Base):
#     __abstract__ = True

#     current_status = db.Column(db.String(50), nullable=False)  # {0: 'delivered', 1 : 'failed', 2 : 'opened'}
#     raw_status = db.Column(db.String(50), nullable=False)
#     status_list = db.Column(db.JSON, nullable=True)
#     channel_response = db.Column(db.String(500), nullable=True)
#     receiver = db.Column(db.String(250), nullable=False)