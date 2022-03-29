from http import HTTPStatus
from flask import Blueprint, jsonify, request
from app.api.model.cuboid import Cuboid
from app.api.schema.cuboid import CuboidSchema
from app.api.db import db
from app.api.model.bag import Bag

cuboid_api = Blueprint("cuboid_api", __name__)


@cuboid_api.route("/", methods=["GET"])
def list_cuboids():
    cuboid_ids = request.args.getlist("cuboid_id")
    cuboid_schema = CuboidSchema(many=True)
    cuboids = Cuboid.query.filter(Cuboid.id.in_(cuboid_ids)).all()

    return jsonify(cuboid_schema.dump(cuboids)), HTTPStatus.OK


@cuboid_api.route("/<int:cuboid_id>", methods=["GET"])
def get_cuboid(cuboid_id):
    cuboid_schema = CuboidSchema()
    cuboid = Cuboid.query.get(cuboid_id)
    
    if cuboid is None:
        return "",HTTPStatus.NOT_FOUND
    
    return jsonify(cuboid_schema.dump(cuboid)), HTTPStatus.OK


@cuboid_api.route("/", methods=["POST"])
def create_cuboid():
    content = request.json

    #create te cuboid
    cuboid_schema = CuboidSchema()
    cuboid = Cuboid(
        width=content["width"],
        height=content["height"],
        depth=content["depth"],
        bag_id=content["bag_id"],
    )
    
    #Bag Validation
    bag_id = content["bag_id"]
    bag = Bag.query.get(bag_id)
    if bag is None:
        return "",HTTPStatus.NOT_FOUND
    
    #Bag space validation
    if bag.available_volume - cuboid.volume < 0:
        return {'message':'Insufficient capacity in bag'}, HTTPStatus.UNPROCESSABLE_ENTITY
    
    db.session.add(cuboid)
    db.session.commit()

    return jsonify(cuboid_schema.dump(cuboid)), HTTPStatus.CREATED


@cuboid_api.route("/<int:cuboid_id>", methods=["PUT"])
def update_cuboid(cuboid_id):
    try:
        content = request.json
        cuboid_schema = CuboidSchema()
        
        #CUboid ID validation
        cuboid = Cuboid.query.get(cuboid_id)
        if cuboid is None:
            return {'message':'Cuboid Not found'},HTTPStatus.NOT_FOUND
        
        #Bag id validation
        bag_id = content.get("bag_id",cuboid.bag_id)
        bag = Bag.query.get(bag_id)
        if cuboid is None:
            return {'message':'Bag Not found'},HTTPStatus.NOT_FOUND
        
        cuboid.width = content.get("width",cuboid.width)
        cuboid.height  = content.get("height",cuboid.height)
        cuboid.depth = content.get("depth",cuboid.depth)
        cuboid.bag_id  = bag_id
        
        #validate the bag space
        if bag.available_volume < 0:
            return {'message':'Cuboid exceeds bag available volume'},HTTPStatus.UNPROCESSABLE_ENTITY
        
        #Data validation
        data_to_load = cuboid_schema.dump(cuboid)
        cuboid_schema.load(data_to_load)

        #update cuboid
        db.session.commit()

        return jsonify(cuboid_schema.dump(cuboid)), HTTPStatus.OK
    except Exception as error:
        return {'message':str(error)},HTTPStatus.INTERNAL_SERVER_ERROR

@cuboid_api.route("/<int:cuboid_id>", methods=["DELETE"])
def delete_cuboid(cuboid_id):
    try:
        cuboib = Cuboid.query.get(cuboid_id)
        
        if cuboib is None:
            return {'message':f'Cuboid {cuboid_id} does not exist'},HTTPStatus.NOT_FOUND
        
        #delete the cuboid
        db.session.delete(cuboib)
        db.session.commit()
        
        return "",HTTPStatus.OK
    
    except Exception as error:
        return {'message':str(error)},HTTPStatus.INTERNAL_SERVER_ERROR
