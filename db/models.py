from ormar import Model, Integer, String, DateTime, JSON
from .database import database, metadata
from datetime import datetime


class User(Model):
    class Meta:
        database = database
        metadata = metadata
        tablename = "users"

    id: int = Integer(primary_key=True)
    username: str = String(max_length=100)
    created_at: datetime = DateTime(default=datetime.now)
    data: dict = JSON(default={})
