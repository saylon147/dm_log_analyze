from flask import Flask
import mongoengine as me
from routes.api import api

MONGO_URI = 'mongodb://localhost:27017/dm_logs'


def init_db(url):
    me.connect(host=url)


def create_app():
    app = Flask(__name__)

    init_db(MONGO_URI)

    app.register_blueprint(api, url_prefix="/api")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
