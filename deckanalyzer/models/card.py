import sqlalchemy
from deckanalyzer import models


class Card(models.Base):
    """
    Card Model
    """
    __tablename__ = "card"

    id = sqlalchemy.Column(
        sqlalchemy.Integer(),
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
    text = sqlalchemy.Column(
        sqlalchemy.String(512),
        nullable=True
    )
    power = sqlalchemy.Column(
        sqlalchemy.SmallInteger(),
        nullable=True
    )
    toughness = sqlalchemy.Column(
        sqlalchemy.SmallInteger(),
        nullable=True
    )
    is_artifact = sqlalchemy.Column(
        sqlalchemy.Boolean(),
        default=False
    )
    is_creature = sqlalchemy.Column(
        sqlalchemy.Boolean(),
        default=False
    )
    is_enchantment = sqlalchemy.Column(
        sqlalchemy.Boolean(),
        default=False
    )
    is_instant = sqlalchemy.Column(
        sqlalchemy.Boolean(),
        default=False
    )
    is_land = sqlalchemy.Column(
        sqlalchemy.Boolean(),
        default=False
    )
    is_planeswalker = sqlalchemy.Column(
        sqlalchemy.Boolean(),
        default=False
    )
    is_sorcery = sqlalchemy.Column(
        sqlalchemy.Boolean(),
        default=False
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
        {"mysql_charset": "utf8mb4", "schema": "gathering"}
    )
