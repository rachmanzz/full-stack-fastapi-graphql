from datetime import datetime
import sqlalchemy as sa
from app.core.config import settings

metadata = sa.MetaData()

users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("email", sa.String, nullable=False),
    sa.Column("hashed_password", sa.String, nullable=False),
    sa.Column("created_date", sa.DateTime)
)

items = sa.Table(
    "items",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("title", sa.String, nullable=False),
    sa.Column("description", sa.String, nullable=True),
    sa.Column("owner_id", sa.Integer, nullable=False),
    sa.Column("created_date", sa.DateTime)
)

engine = sa.create_engine(
    settings.SQLALCHEMY_DATABASE_URI, connect_args={}, echo=True
)
metadata.create_all(engine)
