from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from marshmallow import Schema, fields

import os


# This method to get an absolute path of a file works with all the operative systems.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#DB_URI = "sqlite:///" + os.path.join(BASE_DIR, "database.db")
DB_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
        username="",
        password="",
        hostname="",
        databasename="")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Framework(db.Model):
    __tablename__ = "frameworks"

    # The id will be unique, cannot be null, and auto-increase.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

class Link(db.Model):
    __tablename__ = "links"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100))

class FrameworkSchema(Schema):
    id = fields.Int()
    name = fields.Str()
        
class LinkSchema(Schema):
    id = fields.Int()
    link = fields.Str()

@app.route("/")
def index():

    return "Hello World!"


# GET METHOD

@app.route("/api/frameworks/", methods=["GET"])
def get_frameworks():
    frameworks = Framework.query.all()
    frameworks_schema = FrameworkSchema(many=True)
    result, errors = frameworks_schema.dump(frameworks)

    return jsonify(result)

@app.route("/api/frameworks/<string:name>")
def get_framework_by_name(name):
    framework = Framework.query.filter_by(name=name).first()
    framework_dict = dict(id=framework.id, name=framework.name)

    return jsonify(framework_dict)


# POST METHOD

@app.route("/api/frameworks/", methods=["POST"])
def add_framework():
    new_framework = Framework(name=request.json["name"])
    db.session.add(new_framework)
    db.session.commit()

    framework_dict = dict(id=new_framework.id, name=new_framework.name)

    return jsonify(framework_dict)


# PUT METHOD

@app.route("/api/frameworks/<int:id>", methods=["PUT"])
def edit_framework(id):
    framework = Framework.query.get(id)
    framework.name = request.json["name"]

    db.session.commit()

    framework_dict = dict(id=framework.id, name=framework.name)

    return jsonify(framework_dict)


# DELETE METHOD

@app.route("/api/frameworks/<int:id>", methods=["DELETE"])
def delete_framework(id):
    framework = Framework.query.get(id)
    
    db.session.delete(framework)
    db.session.commit()

    return jsonify({"message": "ok"})


#LINKS

@app.route("/api/links/", methods=["GET"])
def get_links():
    links = Link.query.all()
    links_schema = LinkSchema(many=True)
    result, errors = links_schema.dump(links)

    return jsonify(result)

@app.route("/api/links/<string:url>")
def get_link_by_url(url):
    link = Link.query.filter_by(url=url).first()
    link_dict = dict(id=link.id, url=link.url)

    return jsonify(link_dict)


# POST METHOD

@app.route("/api/links/", methods=["POST"])
def add_link():
    new_link = Link(url=request.json["url"])
    db.session.add(new_link)
    db.session.commit()

    link_dict = dict(id=new_link.id, url=new_link.url)

    return jsonify(link_dict)


# PUT METHOD

@app.route("/api/links/<int:id>", methods=["PUT"])
def edit_link(id):
    link = Link.query.get(id)
    link.url = request.json["url"]

    db.session.commit()

    link_dict = dict(id=link.id, url=link.url)

    return jsonify(link_dict)


# DELETE METHOD

@app.route("/api/links/<int:id>", methods=["DELETE"])
def delete_link(id):
    link = Link.query.get(id)
    
    db.session.delete(link)
    db.session.commit()

    return jsonify({"message": "ok"})
