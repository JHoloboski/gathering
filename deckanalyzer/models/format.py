import sqlalchemy
from deckanalyzer import models


class Format(models.Base):
    """
    Format Model
    """
    __tablename__ = "format"

    id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        nullable=False,
        autoincrement=True,
        primary_key=True
    )
    name = sqlalchemy.Column(
        sqlalchemy.String(128),
        default=None
    )
    start_datetime = sqlalchemy.Column(
        sqlalchemy.DateTime(),
        default=None
    )
    end_datetime = sqlalchemy.Column(
        sqlalchemy.DateTime(),
        default=None
    )
    # id that mtgdecks.net uses, might be culled later
    external_id = sqlalchemy.Column(
        sqlalchemy.SmallInteger(),
        default=0
    )

    deck = sqlalchemy.orm.relationship(
        "Deck",
        backref="format",
        primaryjoin="Deck.format_id == Format.id",
        foreign_keys="[Deck.format_id]",
        passive_deletes="all",
        uselist=False
    )

    __table_args__ = (
        {"mysql_charset": "utf8mb4", "schema": "gathering"}
    )
