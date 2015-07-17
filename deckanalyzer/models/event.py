import sqlalchemy
from deckanalyzer import models
from deckanalyzer.models import format


class Event(models.Base):
    """
    Event Model
    """
    __tablename__ = "event"

    id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        autoincrement=True,
        primary_key=True
    )
    event_datetime = sqlalchemy.Column(
        sqlalchemy.DateTime(),
        default=None
    )
    format_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey(
            format.Format.id,
            onupdate="CASCADE",
            ondelete="SET NULL"
        )
    )
    number_of_players = sqlalchemy.Column(
        sqlalchemy.SmallInteger(),
        default=0
    )

    __table_args__ = (
        sqlalchemy.Index(
            "event_datetime_idx",
            event_datetime
        ),
        {"mysql_charset": "utf8mb4", "schema": "gathering"}
    )
