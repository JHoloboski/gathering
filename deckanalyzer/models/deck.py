import sqlalchemy


class Card(object):
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
    rank = sqlalchemy.Column(
        sqlalchemy.SmallInteger(),
        nullable=False
    )

    __table_args__ = (
        sqlalchemy.Index(
            "rank_idx",
            rank
        ),
        {"mysql_charset": "utf8mb4"}
    )
