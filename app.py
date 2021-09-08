"""Flask app for Cupcakes"""
from flask import Flask, json,request,redirect,render_template,jsonify
from models import Cupcake, db, connect_db,pg_user, pg_pwd
app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{username}:{password}@localhost:5432/cupcakes_db".format(username=pg_user, password=pg_pwd)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'welcomehomesir'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=True


connect_db(app)
db.create_all()

from flask_sqlalchemy import SQLAlchemy

pg_user = "tester"
pg_pwd = "testing123"

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app) 

@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/api/cupcakes')
def get_all_cupcakes():
    all_cupcakes = Cupcake.query.all()
    data = [cupcake.serialize() for cupcake in all_cupcakes]
    return jsonify(cupcakes=data)

@app.route('/api/cupcakes/<cupcake_id>')
def cupcake_details(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()
    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=['POST'])
def new_cupcake():
    print(request.json)
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']
    new_cupcake = Cupcake(flavor=flavor,size=size,rating=rating,image=image)
    db.session.add(new_cupcake)
    db.session.commit()
    serialized = new_cupcake.serialize()
    return (jsonify(cupcake=serialized), 201)

@app.route('/api/cupcakes/<cupcake_id>', methods=['PATCH'])
def cupcake_update(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json['flavor']
    cupcake.size = request.json['size']
    cupcake.rating = request.json['rating']
    cupcake.image = request.json['image']
    db.session.add(cupcake)
    db.session.commit()
    serialized = cupcake.serialize()
    return jsonify(cupcake=serialized)


@app.route('/api/cupcakes/<cupcake_id>', methods=['DELETE'])
def cupcake_delete(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify({'message':'Deleted'})