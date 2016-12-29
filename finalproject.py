from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import session_maker

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantcatalog.db')
Base.metadata.bind = engine

DBSession = session_maker(bind = engine)
session = DBSession()

# This module will display all the restaurants #CHECKED
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

# This module display the menu items of a restaurant
@app.route('/restaurant/<int:restaurant_id>/')
def showRestaurantMenu(restaurant_id):
    menuitems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return render_template('menu.html', menuitems = menuitems)

# This module will edit the current restaurant name
@app.route('/editrestaurant/<int:restaurant_id>/', methods = ['GET','POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        restaurant.name = request.form['newResName']
        session.add(restaurant)
        session.commit()
        flash('Restaurant Successfully edited !!')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editrestaurant.html', restaurant = restaurant)

# This module add a new restaurant to the database
@app.route('/newrestaurant/', methods=['GET','POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['newResName'])
        session.add(newRestaurant)
        session.commit()
        flask('New Restaurant added Successfully !!')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newrestaurant.html')

# This module delete the restaurant from the database
@app.route('/deleterestaurant/<int:restaurant_id>/', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        menuitems = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
        session.delete(menuitems)
        session.delete(restaurant)
        session.commit()
        flask('Restaurant deleted Successfully !!')
    else:
        return render_template('deleterestaurant.html', restaurant = restaurant)

# This module will display all the menu items
@app.route('/menuitems/')
def showAllMenuItems():
    menuitems = session.query(MenuItem).all()
    return render_template('menuitems.html', menuitems = menuitems)

# This module add new menu item in the database
@app.route('/newmenuitem/<int:restaurant_id>/', methods = ['GET','POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        newMenuItem = MenuItem(name = request.form['newMenuName'],
        description = request.form['description'],
        price = request.form['price'], course = request.form['course'], restaurant_id = restaurant.id )
        session.add(newMenuItem)
        session.commit()
        flask("New menu item added Successfully !!")
    else:
        return render_template('newmenuitem.html', restaurant = restaurant)

# This module edit the menu item in the database
@app.route('/editmenuitem/<int:menu_id>/', methods = ['GET','POST'])
def editMenuItem(menu_id):
    menuitem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        menuitem.name = request.form['newMenuName']
        menuitem.description = request.form['description']
        menuitem.price = request.form['price']
        menuitem.price = request.form['course']
        session.add(menuitem)
        session.commit()
        flask('Menu item edited successfully !!')
    else:
        return render_template('editmenuitem.html', menuitem = menuitem)

@app.route('/deletemenuitem/<int:menu_id>/', methods=['GET','POST'])
def deleteMenuItem(menu_id):
    menuitem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(menuitem)
        session.commit()
        flask('Menu Item deleted successfully !!')
    else:
        return render_template('deletemenuitem.html', menuitem = menuitem)



if __name__ == '__main__':
    # secret_key will be used for session
    app.secret_key = "hello_fsnd"
    app.run(host='0.0.0.0', port=5000, debug=True)
