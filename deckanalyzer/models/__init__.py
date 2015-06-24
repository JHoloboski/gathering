import sqlalchemy
from sqlalchemy import orm

from contextlib import contextmanager

# grab from config or command line argument later
engine = sqlalchemy.create_engine("mysql://root:@localhost/gathering")
Session = orm.sessionmaker(bind=engine, autoflush=True)


@contextmanager
def session():
    """
    Context manager based session
    :returns: Session

    """
    try:
        sess = Session()
        yield sess
        sess.commit()
    except:
        sess.rollback()
        raise
    finally:
        sess.close()
