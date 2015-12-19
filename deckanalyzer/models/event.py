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
    name = sqlalchemy.Column(
        sqlalchemy.String()
    )
    event_date = sqlalchemy.Column(
        sqlalchemy.Date(),
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
            "event_date_idx",
            event_date
        ),
        sqlalchemy.UniqueConstraint(
            name,
            event_date,
            name="name_event_date_uidx"
        ),
        {"mysql_charset": "utf8mb4", "schema": "gathering"}
    )
