from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship

Base = declarative_base()


# User table to store users data
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key = True)
    email = Column(String(200), unique = True, nullable = False)
    name = Column(String(200), nullable = True)
    avatar = Column(String(400), nullable = True)


# Restaurant table to store restaurants data
class Restaurant(Base):
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key = True)
    name = Column(String(450), nullable = False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
        }


# Menuitem table to store menu item data
class MenuItem(Base):
    __tablename__ = "menuitem"
    id = Column(Integer, primary_key = True)
    name = Column(String(400), nullable = False)
    description = Column(String(450), nullable = True)
    price = Column(Integer, nullable = True)
    course = Column(String(450), nullable = True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

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

# engine = create_engine('sqlite:///restaurantcatalog.db')
engine = create_engine('postgresql://catalog:abhaypass@localhost/catalog')
Base.metadata.create_all(engine)
