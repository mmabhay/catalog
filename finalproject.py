from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import session_maker

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantcatalog.db')
Base.metadata.bind = engine

DBSession = session_maker(bind = engine)
session = DBSession()

# This module will display all the restaurants
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

# This module will display all the menu items
@app.route('/menuitems/')
def showAllMenuItems():
    menuitems = session.query(MenuItem).all()
    return render_template('menuitems.html', menuitems = menuitems)

@app.route('/editrestaurant/<int:restaurant_id>', methods = ['GET','POST'])
def editRestaurant(restaurant_id):
    if request.method == 'POST':





if __name__ == '__main__':
    # secret_key will be used for session
    app.secret_key = "hello_fsnd"
    app.run(host='0.0.0.0', port=5000, debug=True)
