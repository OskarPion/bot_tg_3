import ormar
import datetime
from .database import ormar_base_config


class User(ormar.Model):
    ormar_config = ormar_base_config.copy()

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    tg_id: int = ormar.BigInteger(unique=True, nullable=False)
    username: str = ormar.String(max_length=200, nullable=True)
    name: str = ormar.String(max_length=250)
    created_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now())
    style: str = ormar.String(max_length=6000, nullable=True)
    passed_setup: str = ormar.Boolean(default=False)
    email: str = ormar.String(max_length=100, nullable=True)
    has_subscription: bool = ormar.Boolean(default=False)
    current_dialog_id: int = ormar.Integer(nullable=True)
