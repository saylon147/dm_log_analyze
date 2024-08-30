from flask import Flask, Blueprint
import mongoengine as me

from backend.routes.query import query
from backend.routes.upload import upload

MONGO_URI = 'mongodb://localhost:27017/dm_logs'

app = Flask(__name__)
api = Blueprint('api', __name__)

me.connect(host=MONGO_URI)

app.register_blueprint(query, url_prefix="/query")
app.register_blueprint(upload, url_prefix="/upload")

if __name__ == "__main__":
    app.run(debug=True)
