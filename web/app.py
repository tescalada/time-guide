
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/info')
def planet_info():

    # get the name of the planet passed in
    # via the url at /info?planet=PLANETNAME
    planet = request.args.get("planet")

    # some data about the planets
    planet_data = {
        "mercury": {
            "size": 2440,
        },
        "venus": {
            "size": 6052,
        },
        "earth": {
            "size": 6371,
        },
        "mars": {
            "size": 3390,
        },
        "jupiter": {
            "size": 69911,
        },
        "saturn": {
            "size": 58232,
        },
        "uranus": {
            "size": 25362,
        },
        "neptune": {
            "size": 24622,
        },
    }

    # return json with the planet name and the
    # size looked up from the panet_data dict
    return jsonify(
        name=planet,
        size=planet_data[planet]['size'],
    )


if __name__ == '__main__':
    app.run()
