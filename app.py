from flask import Flask, redirect, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus

app = Flask(__name__)
modus = Modus(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/bootcamp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Bootcamp(db.Model):

    __tablename__ = 'bootcamps'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    location = db.Column(db.Text)
    votes = db.Column(db.Integer)

    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.votes = 0

##ROUTES
@app.route('/')
def root():
    return redirect(url_for('index'))

@app.route('/bootcamps')
def index():
    return render_template('index.html', bootcamps=Bootcamp.query.all());


@app.route('/bootcamps/new')
def new():
    return render_template('new.html')

@app.route('/bootcamps', methods=["POST"])
def create():
    name = request.form.get("name")
    location = request.form.get("location")
    db.session.add(Bootcamp(name, location))
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/bootcamps/<int:id>', methods=["GET"])
def show(id):
    bootcamp = Bootcamp.query.get(id)
    return render_template('show.html', bootcamp=bootcamp)

@app.route('/bootcamps/<int:id>/edit')
def edit(id):
    bootcamp = Bootcamp.query.get(id)
    return render_template('edit.html', bootcamp=bootcamp)

@app.route('/bootcamps/<int:id>', methods=["PATCH"])
def update(id):
    bootcamp = Bootcamp.query.get(id)
    bootcamp.name = request.form.get("name")
    bootcamp.location = request.form.get("location")
    db.session.add(bootcamp)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/bootcamps/<int:id>/vote', methods=["PATCH"])
def vote(id):
    bootcamp = Bootcamp.query.get(id)
    data = request.form
    if(data.get("votes") == 'increment'):
        bootcamp.votes += 1
    else:
        bootcamp.votes -= 1
    db.session.add(bootcamp)
    db.session.commit()
    return jsonify({'votes': bootcamp.votes})

# @app.route('/bootcamps/<int:id>/votedown', methods=["PATCH"])
# def vote_Down(id):
#     bootcamp = Bootcamp.query.get(id)
#     bootcamp.votes -= 1
#     db.session.add(bootcamp)
#     db.session.commit()
#     return jsonify({'votes': bootcamp.votes})

@app.route('/bootcamps/<int:id>', methods=["DELETE"])
def destroy(id):
    bootcamp = Bootcamp.query.get(id)
    db.session.delete(bootcamp)
    db.session.commit()
    return jsonify({'value': 'key'})


