from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key = True)
    email = Column(String(100), unique = True, nullable = False)
    name = Column(String(100), nullable = True)
    avatar = Column(String(200))

class Restaurant(Base):
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
        }

class MenuItem(Base):
    __tablename__ = "menuitem"
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    description = Column(String(250), nullable = False)
    price = Column(Integer, nullable = False)
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'description' : self.description,
            'price' : self.price,
            'course' : self.course,
            'restaurant_id' : self.restaurant_id,
        }

engine = create_engine('sqlite:///restaurantcatalog.db')
Base.metadata.create_all(engine)
