import sqlalchemy
from deckanalyzer import models


class Card(models.Base):
    """
    Card Model
    """
    __tablename__ = "card"

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
    mana_cost = sqlalchemy.Column(
        sqlalchemy.String(32),
        nullable=True
    )
    # converted mana cost, cmc is the well-understood abbreviation of this
    cmc = sqlalchemy.Column(
        sqlalchemy.SmallInteger(),
        nullable=True
    )
    types = sqlalchemy.Column(
        sqlalchemy.String(128),
        nullable=False
    )
    text = sqlalchemy.Column(
        sqlalchemy.String(512),
        nullable=False
    )
    power = sqlalchemy.Column(
        sqlalchemy.SmallInteger(),
        nullable=True
    )
    toughness = sqlalchemy.Column(
        sqlalchemy.SmallInteger(),
        nullable=True
    )

    __table_args__ = (
        sqlalchemy.Index(
            "name_idx",
            name
        ),
        sqlalchemy.Index(
            "cmc_idx",
            cmc
        ),
        {"mysql_charset": "utf8mb4"}
    )
