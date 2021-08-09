from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from db import db
from resources.item import Item, ItemList
from resources.user import User, UserRegister, UserLogin, TokenRefresh, UserLogout
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_SECRET_KEY'] = 'Akash'
api = Api(app)
jwt = JWTManager(app)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(User, '/user/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')


@app.before_first_request
def create_tables():
    db.create_all()


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in BLACKLIST


db.init_app(app)
app.run(port=5000, debug=True)
