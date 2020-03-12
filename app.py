from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.homepage import Homepage

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'saphir09'
api = Api(app)

api.add_resource(Homepage, '/')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
