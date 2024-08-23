from flask import Flask, Blueprint
import mongoengine as me

MONGO_URI = 'mongodb://localhost:27017/dm_logs'

app = Flask(__name__)
api = Blueprint('api', __name__)

me.connect(host=MONGO_URI)

app.register_blueprint(api, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
