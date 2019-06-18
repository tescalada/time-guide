
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/jupiter')
def jupiter_info():
    return jsonify(
        name='Jupiter',
        size='huge',
    )


if __name__ == '__main__':
    app.run()
