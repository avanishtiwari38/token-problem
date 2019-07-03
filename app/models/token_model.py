from .base_model import *
from .serialiser import BaseSchema


class Service(Base):
    __tablename__ = "token"
    token_id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(50), nullable=False, unique=True)
    assigned = db.Column(db.Boolean, nullable=True)
    deleted = db.Column(db.Boolean, default=False)