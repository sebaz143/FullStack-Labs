from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from app.api.db import db
from app.api.model.cuboid import Cuboid


class Bag(db.Model):
    __tablename__ = "bags"

    id = db.Column(db.Integer, primary_key=True)
    volume = db.Column(db.Integer)
    title = db.Column(db.String(255), nullable=True)
    cuboids = db.relationship(Cuboid, backref="bag")
    
    @hybrid_method
    def cal_payload_volume(self):
        bag_payload_volumen = 0
        
        for cub_in_bag in self.cuboids:
            bag_payload_volumen += cub_in_bag.volume
        
        return bag_payload_volumen
    
    @hybrid_property
    def payload_volume(self):
        return self.cal_payload_volume()
    
    @hybrid_property
    def available_volume(self):
        return self.volume - self.cal_payload_volume()

    
