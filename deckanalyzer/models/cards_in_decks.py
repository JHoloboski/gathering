import sqlalchemy


class CardsInDecks(object):
    """
    Card and Deck Relationship Model
    """
    __tablename__ = "cards_in_decks"

    deck_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey("deck.id"),
        nullable=False,
        primary_key=True,

    )
    card_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey("card.id"),
        nullable=False,
        primary_key=True
    )
    count = sqlalchemy.Column(
        sqlalchemy.SmallInteger(),
        nullable=False
    )

    __table_args__ = (
        {"mysql_charset": "utf8mb4"}
    )
