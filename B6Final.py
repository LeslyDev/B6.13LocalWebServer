import os
import json
import album

from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

RESOURCES_PATH = "users/"


def save_user(user_data):
    alb = album.Album(
        artist=user_data["artist"],
        year=user_data["year"],
        genre=user_data["genre"],
        album=user_data["album"]
    )
    try:
        int(alb.year)
    except ValueError:
        return "Год введен некорректно!"
    album_list = album.find(alb.artist)
    album_name = [album.album for album in album_list]
    if alb.album in album_name:
        message = "Альбомов {} не найдено"
        result = HTTPError(409, message)
        print('Альбом {} уже есть в списке'.format(alb.album))
        return result
    album.main(alb)


@route("/user", method="POST")
def user():
    user_data = {
        "artist": request.forms.get("artist"),
        "year": request.forms.get("year"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album")
    }
    a = save_user(user_data)
    if a is not None:
        return a
    return "Данные успешно сохранены"


@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Список альбомов {}\n".format(artist)
        result += "\n".join(album_names)
    return result


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
