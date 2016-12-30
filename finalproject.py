from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database_setup import Base, Restaurant, MenuItem, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

# This module will display all the restaurants
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

# This module display the menu items of a restaurant
@app.route('/restaurant/<int:restaurant_id>/')
def showRestaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    menuitems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return render_template('menu.html', restaurant = restaurant, menuitems = menuitems)

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
        flash('New Restaurant added Successfully !!')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newrestaurant.html')

# This module delete the restaurant from the database
@app.route('/deleterestaurant/<int:restaurant_id>/', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        menuitems = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
        for menuitem in menuitems:
            session.delete(menuitem)
        session.delete(restaurant)
        session.commit()
        flash('Restaurant deleted Successfully !!')
        return redirect(url_for('showRestaurants'))
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
        flash("New menu item added Successfully !!")
        return redirect(url_for('showRestaurantMenu', restaurant_id = restaurant.id))
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
        menuitem.course = request.form['course']
        session.add(menuitem)
        session.commit()
        flash('Menu item edited successfully !!')
        return redirect(url_for('showRestaurantMenu', restaurant_id = menuitem.restaurant_id))
    else:
        return render_template('editmenuitem.html', menuitem = menuitem)

@app.route('/deletemenuitem/<int:menu_id>/', methods=['GET','POST'])
def deleteMenuItem(menu_id):
    menuitem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(menuitem)
        session.commit()
        flash('Menu Item deleted successfully !!')
        return redirect(url_for('showRestaurantMenu', restaurant_id = menuitem.restaurant_id))
    else:
        return render_template('deletemenuitem.html', menuitem = menuitem)

CLIENT_ID = json.loads(open('client_secret.json','r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"

@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE = state)

@app.route('/gconnect', methods = [POST])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope = '')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Getting user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token':credentials.access_token, 'alt':'json'}
    answer = request.get(userinfo_url, params = params)

    data = answer.json()

    login_session['name'] = data['name']
    login_session['email'] = data['email']
    login_session['avatar'] = data['picture']

    # Check to see if user exits in DB
    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['name']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['avatar']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['name'])
    print "done!"
    return output

# Disconnect current user session
@app.route('/gdisconnect/')
def gdisconnect():
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == 200:
        del login_session['credentials']
        del login_session['name']
        del login_session['gplus_id']
        del login_session['email']
        del login_session['avatar']
        response = make_response(json.dumps('Successfully Disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# User Helper functions
def createUser(login_session):
    newUser = User(name = login_session['name'], email = login_session['email'], avatar = login_session['avatar'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email = login_session['email']).one()
    return user

def getUserId(email):
    try:
        user = session.query(User).filter_by(email = email).one()
        return user.id
    except:
        return None

def getUserInfo(user_id):
    user = session.query(User).filter_by(id = user_id).one()
    return user

if __name__ == '__main__':
    # secret_key will be used for session
    app.secret_key = "hello_fsnd"
    app.run(host='0.0.0.0', port=5000, debug=True)
