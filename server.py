import os

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager
from flask_cors import CORS

DB_PATH = 'sqlite:///' + os.path.dirname(os.path.abspath(__file__)) + '/winners_full.db'

app = Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
db = SQLAlchemy(app)
cors = CORS(app)


class Winner(db.Model):
    __tablename__ = 'winner'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('winner.id'), nullable=True)
    name = db.Column(db.Unicode)
    children = db.relationship('Winner')

    #timestamp

    def __init__(self, id, name):  # , *children):
        self.id = id
        self.name = name
        # self.children = children


def get_preprocessor(search_params=None, **kw):
    if search_params is None:
        return
    filter_nonnull = dict(name='parent_id', op='is_null')
    order_alphabetically = dict(field='name', direction='asc')

    if 'filters' not in search_params:
        search_params['filters'] = []
    search_params['filters'].append(filter_nonnull)
    if 'order_by' not in search_params:
        search_params['order_by'] = []
    search_params['order_by'].append(order_alphabetically)



if __name__ == '__main__':
    mr_manager = APIManager(app=app, flask_sqlalchemy_db=db)
    mr_manager.create_api(Winner,
                          methods=['GET', 'PATCH'],
                          preprocessors=dict(GET_MANY=[get_preprocessor]))
    app.run(debug=True)
