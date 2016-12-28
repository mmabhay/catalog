from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import session_maker

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantcatalog.db')
Base.metadata.bind = engine

DBSession = session_maker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/restaurant')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

if __name__ == '__main__':
    # secret_key will be used for session
    app.secret_key = "hello_fsnd"
    app.run(host='0.0.0.0', port=5000, debug=True)
