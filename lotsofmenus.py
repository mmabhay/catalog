from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem, User

# engine = create_engine('sqlite:///restaurantcatalog.db')
engine = create_engine('postgresql://catalog:abhaypass@localhost/catalog')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Users
user1 = User(name = "Abhay Chauhan", email = "abhay.chauhan_1995@hotmail.com")
session.add(user1)
session.commit()

user2 = User(name = "Nakul Chauhan", email = "nakulemail@gmail.com")
session.add(user2)
session.commit()

user3 = User(name = "Anjani Chauhan", email = "anjanichauhan@gmail.com")
session.add(user3)
session.commit()

user4 = User(name = "T.S.Chauhan", email = "tschauhan2006@yahoo.co.in")
session.add(user4)
session.commit()

#Menu for UrbanBurger
restaurant1 = Restaurant(name = "Urban Burger", user = user1)

session.add(restaurant1)
session.commit()


menuItem1 = MenuItem(name = "French Fries", description = "with garlic and parmesan", price = "2", course = "Appetizer", restaurant = restaurant1, user = user1)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(name = "Chicken Burger", description = "Juicy grilled chicken patty with tomato mayo and lettuce", price = "5", course = "Entree", restaurant = restaurant1, user = user1)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(name = "Chocolate Cake", description = "fresh baked and served with ice cream", price = "3", course = "Dessert", restaurant = restaurant1, user = user1)

session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(name = "Sirloin Burger", description = "Made with grade A beef", price = "7", course = "Entree", restaurant = restaurant1, user = user1)

session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(name = "Root Beer", description = "16oz of refreshing goodness", price = "1", course = "Beverage", restaurant = restaurant1, user = user1)

session.add(menuItem5)
session.commit()

menuItem6 = MenuItem(name = "Iced Tea", description = "with Lemon", price = "9", course = "Beverage", restaurant = restaurant1, user = user1)

session.add(menuItem6)
session.commit()

menuItem7 = MenuItem(name = "Grilled Cheese Sandwich", description = "On texas toast with American Cheese", price = "9", course = "Entree", restaurant = restaurant1, user = user1)

session.add(menuItem7)
session.commit()

menuItem8 = MenuItem(name = "Veggie Burger", description = "Made with freshest of ingredients and home grown spices", price = "9", course = "Entree", restaurant = restaurant1, user = user1)

session.add(menuItem8)
session.commit()




#Menu for Super Stir Fry
restaurant2 = Restaurant(name = "Super Stir Fry", user = user2)

session.add(restaurant2)
session.commit()


menuItem1 = MenuItem(name = "Chicken Stir Fry", description = "with your choice of noodles vegetables and sauces", price = "9", course = "Entree", restaurant = restaurant2, user = user2)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(name = "Peking Duck", description = " a famous duck dish from in front of the diners by the cook", price = "25", course = "Entree", restaurant = restaurant2, user = user2)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(name = "Spicy Tuna Roll", description = "", price = "2", course = "", restaurant = restaurant2, user = user2)

session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(name = "Nepali Momo ", description = "", price = "2", course = "", restaurant = restaurant2, user = user2)

session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(name = "Beef Noodle Soup", description = "", price = "2", course = "", restaurant = restaurant2, user = user2)

session.add(menuItem5)
session.commit()

menuItem6 = MenuItem(name = "Ramen", description = "", price = "", course = "2", restaurant = restaurant2, user = user2)

session.add(menuItem6)
session.commit()




#Menu for Panda Garden
restaurant1 = Restaurant(name = "Panda Garden", user = user3)

session.add(restaurant1)
session.commit()


menuItem1 = MenuItem(name = "Pho", description = "a pho, a few herbs, and meat.", price = "1", course = "", restaurant = restaurant1, user = user3)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(name = "Chinese Dumplings", description = "a common skin can be either thin and elastic or thicker.", price = "1", course = "", restaurant = restaurant1, user = user3)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(name = "Gyoza", description = "The fact that gyoza wrappers are much thinner", price = "1", course = "", restaurant = restaurant1, user = user3)

session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(name = "Stinky Tofu", description = "Taiwanese dish, deep pickled cabbage.", price = "2", course = "", restaurant = restaurant1, user = user3)

session.add(menuItem4)
session.commit()



#Menu for Thyme for that
restaurant1 = Restaurant(name = "Thyme for That Vegetarian Cuisine ", user = user4)

session.add(restaurant1)
session.commit()


menuItem1 = MenuItem(name = "Tres Leches Cake", description = "Rich, bean whipped cream and strawberries.", price = "1", course = "", restaurant = restaurant1, user = user4)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(name = "Mushroom risotto", description = "Portabello mushrooms in a creamy risotto", price = "1", course = "", restaurant = restaurant1, user = user4)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(name = "Honey Boba Shaved Snow", description = "Milk snow layered cream, and freshly made mochi", price = "1", course = "", restaurant = restaurant1, user = user4)

session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(name = "Cauliflower Manchurian", description = "Golden fried celery, chilies,ginger & green onions", price = "2", course = "", restaurant = restaurant1, user = user4)

session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(name = "Aloo Gobi Burrito", description = "Vegan goodness cauliflower (gobi) and chutney. Nom Nom", price = "2", course = "", restaurant = restaurant1, user = user4)

session.add(menuItem5)
session.commit()




#Menu for Tony's Bistro
restaurant1 = Restaurant(name = "Tony\'s Bistro ", user = user1)

session.add(restaurant1)
session.commit()


menuItem1 = MenuItem(name = "Shellfish Tower", description = "", price = "1", course = "", restaurant = restaurant1, user = user1)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(name = "Chicken and Rice", description = "", price = "1", course = "", restaurant = restaurant1, user = user1)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(name = "Mom's Spaghetti", description = "", price = "1", course = "", restaurant = restaurant1, user = user1)

session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(name = "Choc Full O\' Mint (Smitten\'s Fresh Mint Chip ice cream)", description = "", price = "1", course = "", restaurant = restaurant1, user = user1)

session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(name = "Tonkatsu Ramen", description = "Noodles in a broth with a soft-boiled egg", price = "1", course = "", restaurant = restaurant1, user = user1)

session.add(menuItem5)
session.commit()




#Menu for Andala's
restaurant1 = Restaurant(name = "Andala\'s", user = user2)

session.add(restaurant1)
session.commit()


menuItem1 = MenuItem(name = "Lamb Curry", description = "Slow cook that Indian spices. Mmmm.", price = "1", course = "", restaurant = restaurant1, user = user2)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(name = "Chicken Marsala", description = "Chicken cooked in Marsala wine sauce with mushrooms", price = "1", course = "", restaurant = restaurant1, user = user2)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(name = "Potstickers", description = "Delicious chicken and veggies encapsulated in fried dough.", price = "1", course = "", restaurant = restaurant1, user = user2)

session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(name = "Nigiri SamplerMaguro, Sake, Hamachi, Unagi, Uni, TORO!", description = "", price = "1", course = "", restaurant = restaurant1, user = user2)

session.add(menuItem4)
session.commit()




#Menu for Auntie Ann's
restaurant1 = Restaurant(name = "Auntie Ann\'s Diner ", user = user3)

session.add(restaurant1)
session.commit()

menuItem9 = MenuItem(name = "Chicken Fried Steak", description = "Fresh and smothered with cream gravy", price = "8", course = "Entree", restaurant = restaurant1, user = user3)

session.add(menuItem9)
session.commit()



menuItem1 = MenuItem(name = "Boysenberry Sorbet", description = "An unsettlingly huge awesomeness", price = "9", course = "", restaurant = restaurant1, user = user3)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(name = "Broiled salmon", description = "Salmon fillet marinated and broiled hot & fast", price = "1", course = "", restaurant = restaurant1, user = user3)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(name = "Morels on toast (seasonal)", description = "Wild morel mushrooms toast slices", price = "1", course = "", restaurant = restaurant1, user = user3)

session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(name = "Tandoori Chicken", description = "Chicken marinated in burning charcoal.", price = "1", course = "", restaurant = restaurant1, user = user3)

session.add(menuItem4)
session.commit()




#Menu for Cocina Y Amor
restaurant1 = Restaurant(name = "Cocina Y Amor ", user = user4)

session.add(restaurant1)
session.commit()


menuItem1 = MenuItem(name = "Super Burrito Al Pastor", description = "Marinated Cilantro, Salsa, Tortilla", price = "1", course = "", restaurant = restaurant1)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(name = "Cachapa", description = "Golden brown, corn-based and possibly lechon. ", price = "1", course = "", restaurant = restaurant1)

session.add(menuItem2)
session.commit()

print "added menu items!"
