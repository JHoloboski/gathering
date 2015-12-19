import sqlalchemy
from deckanalyzer import models
from deckanalyzer.models import event


class Deck(models.Base):
    """
    Deck Model
    """
    __tablename__ = "deck"

    id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        autoincrement=True,
        primary_key=True
    )
    name = sqlalchemy.Column(
        sqlalchemy.String(128),
        default=None
    )
    event_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey(
            event.Event.id,
            onupdate="CASCADE",
            ondelete="SET NULL"
        )
    )
    rank = sqlalchemy.Column(
        sqlalchemy.SmallInteger(),
        nullable=False
    )
    # WIP way of weighting ranks based on how many participants were
    # in the event this deck was used in
    weighted_rank_value = sqlalchemy.Column(
        sqlalchemy.Numeric(18, 9)
    )
    # the following won't be sideboard inclusive
    lands = sqlalchemy.Column(
        sqlalchemy.SmallInteger(),
        default=0
    )
    non_lands = sqlalchemy.Column(
        sqlalchemy.SmallInteger(),
        default=0
    )
    avg_cmc = sqlalchemy.Column(
        sqlalchemy.Numeric(18, 9),
        default=0.0
    )

    __table_args__ = (
        sqlalchemy.Index(
            "rank_idx",
            rank
        ),
        sqlalchemy.Index(
            "weighted_rank_idx",
            weighted_rank_value
        ),
        sqlalchemy.Index(
            "avg_cmc_idx",
            avg_cmc
        ),
        {"mysql_charset": "utf8mb4", "schema": "gathering"}
    )
