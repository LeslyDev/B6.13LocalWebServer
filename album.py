import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums


def check(artist):
    session = connect_db()
    albums_list = session.query(Album).filter(Album.artist == artist).all()
    alb = [album.album for album in albums_list]
    return alb


def main(user):
    session = connect_db()
    session.add(user)
    session.commit()
    print("Спасибо, данные сохранены!")
