from ma import ma
from models.car import CarModel


class CarSchema(ma.ModelSchema):
    class Meta:
        model = CarModel
        dump_only = ("id",)
