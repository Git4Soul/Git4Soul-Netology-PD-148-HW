from flask import Flask, Response, jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from db import Session, Advertisement
from errors import HttpError
from schema import CreateAdvertisement, UpdateAdvertisement, validate

app = Flask("app")


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_requests(response: Response):
    request.session.close()
    return response


@app.errorhandler(HttpError)
def error_handler(err: HttpError):
    response = jsonify({"error": err.message})
    response.status_code = err.status_code
    return response


def get_advertisement(advertisement_id: int) -> Advertisement:
    advertisement = request.session.get(Advertisement, advertisement_id)
    if advertisement is None:
        raise HttpError("advertisement not found", 404)
    return advertisement


def add_advertisement(advertisement: Advertisement):
    request.session.add(advertisement)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError("advertisement already exists", 400)


class AdvertisementView(MethodView):
    def get(self, advertisement_id: int | None = None):
        if advertisement_id is None:
            advertisements = request.session.query(Advertisement).all()
            return jsonify([ad.dict for ad in advertisements])
        advertisement = get_advertisement(advertisement_id)
        return jsonify(advertisement.dict)

    def post(self):
        json_data = validate(request.json, CreateAdvertisement)
        advertisement = Advertisement(
            title=json_data["title"],
            description=json_data.get("description"),
            owner=json_data["owner"],
        )
        add_advertisement(advertisement)
        return jsonify(advertisement.id_dict), 201

    def patch(self, advertisement_id: int):
        json_data = validate(request.json, UpdateAdvertisement)
        advertisement = get_advertisement(advertisement_id)

        if "title" in json_data:
            advertisement.title = json_data["title"]
        if "description" in json_data:
            advertisement.description = json_data["description"]
        if "owner" in json_data:
            advertisement.owner = json_data["owner"]

        add_advertisement(advertisement)
        return jsonify(advertisement.dict)

    def delete(self, advertisement_id: int):
        advertisement = get_advertisement(advertisement_id)
        request.session.delete(advertisement)
        request.session.commit()
        return jsonify({"message": "deleted"})


advertisement_view = AdvertisementView.as_view("advertisement")

app.add_url_rule(
    "/advertisements",
    view_func=advertisement_view,
    methods=["POST", "GET"],
)
app.add_url_rule(
    "/advertisements/<int:advertisement_id>",
    view_func=advertisement_view,
    methods=["GET", "PATCH", "DELETE"],
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)