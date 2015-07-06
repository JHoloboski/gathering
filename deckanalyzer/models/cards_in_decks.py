import sqlalchemy
from deckanalyzer import models


class CardsInDecks(models.Base):
    """
    Card and Deck Relationship Model
    """
    __tablename__ = "cards_in_decks"

    id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        autoincrement=True,
        primary_key=True
    )
    deck_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey(
            "deck.id",
            onupdate="CASCADE",
            ondelete="SET NULL"
        )
    )
    card_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey(
            "card.id",
            onupdate="CASCADE",
            ondelete="SET NULL"
        )
    )
    main_quantity = sqlalchemy.Column(
        sqlalchemy.SmallInteger(),
        default=0
    )
    side_quantity = sqlalchemy.Column(
        sqlalchemy.SmallInteger(),
        default=0
    )

    __table_args__ = (
        {"mysql_charset": "utf8mb4"}
    )
