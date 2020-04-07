from typing import List

from db import db


class CarModel(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    carname = db.Column(db.String(80), nullable=False, unique=True)
    carType = db.Column(db.String(80), nullable=False)
    carPrice = db.Column(db.Float(precision=2), nullable=False)

    @classmethod
    def find_by_carname(cls, carname: str) -> "CarModel":
        return cls.query.filter_by(carname=carname).first()

    @classmethod
    def find_all(cls) -> List["CarModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
