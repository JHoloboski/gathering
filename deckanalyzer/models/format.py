import sqlalchemy


class Format(object):
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

    __table_args__ = (
        {"mysql_charset": "utf8mb4"}
    )
