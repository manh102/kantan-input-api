from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, fresh_jwt_required
from marshmallow import ValidationError
from models.car import CarModel
from schemas.car import CarSchema

NAME_ALREADY_EXISTS = "An car with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the car."
CAR_NOT_FOUND = "Car not found."
ITEM_DELETED = "Car deleted."

car_schema = CarSchema()
car_list_schema = CarSchema(many=True)

class Car(Resource):

    @classmethod
    def get(cls, carname: str):
        car = CarModel.find_by_carname(carname)
        if car:
            return car_schema.dump(car), 200
        return {"message": CAR_NOT_FOUND}, 404

    @classmethod
    @fresh_jwt_required
    def post(cls, carname: str): # /item/chair
        if CarModel.find_by_carname(carname):
            return {"message": NAME_ALREADY_EXISTS.format(carname)}, 400

        car_json = request.get_json()
        car_json["carname"] = carname

        try:
            car = car_schema.load(car_json)
        except ValidationError as err:
            return err.messages, 400

        try:
            car.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return car_schema.dump(car), 201


class CarList(Resource):
    @classmethod
    def get(cls):
        return {"cars": car_list_schema.dump(CarModel.find_all())}, 200
