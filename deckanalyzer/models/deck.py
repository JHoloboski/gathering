import sqlalchemy
from deckanalyzer import models


class Deck(models.Base):
    """
    Deck Model
    """
    __tablename__ = "deck"

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
    format_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey(
            "format.id",
            onupdate="CASCADE",
            ondelete="SET NULL"
        )
    )
    rank = sqlalchemy.Column(
        sqlalchemy.SmallInteger(),
        nullable=False
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
            "avg_cmc_idx",
            avg_cmc
        ),
        {"mysql_charset": "utf8mb4"}
    )
