from flask import Flask, render_template, request, redirect, url_for
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
from flask import make_response, flash, jsonify
import requests
from functools import wraps

CLIENT_ID = json.loads(open('client_secrets.json','r')
    .read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

# End points

@app.route('/restaurants/JSON/')
def restaurantsEndPoint():
    '''
    restaurantEndPoint : function returns the list of
    restaurants in json format
    '''
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurant = [restaurant.serialize
        for restaurant in restaurants])

@app.route('/menuitems/JSON/')
def menuItemsEndPoint():
    '''
    menuItemsEndPoint : function return the list of menu
    items in json format
    '''
    menuitems = session.query(MenuItem).all()
    return jsonify(MenuItem = [menuitem.serialize
        for menuitem in menuitems])

@app.route('/restaurant/<int:restaurant_id>/JSON/')
def singleRestaurantEndPoint(restaurant_id):
    '''
    singleRestaurantEndPoint : function return json data for
    a particular restaurant.
    '''
    restaurant = session.query(Restaurant).filter_by(
        id == restaurant_id).first()
    return jsonify(Restaurant = restaurant.serialize)

@app.route('/menuitem/<int:menu_id>/JSON/')
def singleMenuItemEndPoint(menu_id):
    '''
    singleMenuItemEndPoint : function return json data of single
    menu item
    '''
    menuitem = session.query(MenuItem).filter_by(id == menu_id).first()
    return jsonify(MenuItem = menuitem.serialize)

def login_required(func):
    '''
    login_required : function decorator for checking if
    user is logged in

    Returns:
        If not logged in, redirects to login page.
    '''
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' in login_session:
            return func(*args, **kwargs)
        else:
            flash("You are not allowed to acces this"
            "without logging in!")
            return redirect("/login/")
    return decorated_function

# This module will display all the restaurants
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

# This module display the menu items of a restaurant
@app.route('/restaurant/<int:restaurant_id>/')
def showRestaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(
        id = restaurant_id).first()
    if restaurant is None:
        return redirect(url_for('showRestaurants'))
    menuitems = session.query(MenuItem).filter_by(
        restaurant_id = restaurant_id).all()
    return render_template('menu.html', restaurant = restaurant,
        menuitems = menuitems)

# This module will edit the current restaurant name
@app.route('/editrestaurant/<int:restaurant_id>/', methods = ['GET','POST'])
@login_required
def editRestaurant(restaurant_id):
    '''
        editRestaurant : function edit restaurant details
    '''
    restaurant = session.query(Restaurant).filter_by(
        id = restaurant_id).first()
    if restaurant is None:
        return redirect(url_for('showRestaurants'))
    if restaurant.user_id != login_session['user_id']:
        return redirect(url_for('showRestaurants'))
    if request.method == 'POST':
        if request.form['newResName'] == "":
            flash("All fields are necessary!!")
            return render_template('editrestaurant.html',
                restaurant = restaurant)
        restaurant.name = request.form['newResName']
        session.add(restaurant)
        session.commit()
        flash('Restaurant Successfully edited !!')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editrestaurant.html',
            restaurant = restaurant)

# This module add a new restaurant to the database
@app.route('/newrestaurant/', methods=['GET','POST'])
@login_required
def newRestaurant():
    '''
        newRestaurant : function add a new restaurant to the database
    '''
    if request.method == 'POST':
        if request.form['newResName'] == "":
            flash("All fields are necessary!!")
            return render_template('newrestaurant.html')
        newRestaurant = Restaurant(name = request.form['newResName'],
            user_id = login_session['user_id'])
        session.add(newRestaurant)
        session.commit()
        flash('New Restaurant added Successfully !!')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newrestaurant.html')

# This module delete the restaurant from the database
@app.route('/deleterestaurant/<int:restaurant_id>/', methods=['GET','POST'])
@login_required
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    if restaurant is None:
        return redirect(url_for('showRestaurants'))
    if restaurant.user_id != login_session['user_id']:
        return redirect(url_for('showRestaurants'))
    if request.method == 'POST':
        menuitems = session.query(MenuItem).filter_by(
            restaurant_id = restaurant.id).all()
        for menuitem in menuitems:
            session.delete(menuitem)
        session.delete(restaurant)
        session.commit()
        flash('Restaurant deleted Successfully !!')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleterestaurant.html',
            restaurant = restaurant)

# This module will display all the menu items
@app.route('/menuitems/')
def showAllMenuItems():
    menuitems = session.query(MenuItem).all()
    return render_template('menuitems.html', menuitems = menuitems)

# This module add new menu item in the database
@app.route('/newmenuitem/<int:restaurant_id>/', methods = ['GET','POST'])
@login_required
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(
        id = restaurant_id).first()

    if restaurant is None:
        return redirect(url_for('showRestaurants'))

    if restaurant.user_id != login_session['user_id']:
        return redirect(url_for('showRestaurantMenu',
            restaurant_id = restaurant.id))

    if request.method == 'POST':
        if (request.form['newMenuName'] != "" and
            request.form['description'] != "" and request.form['price'] != ""
            and request.form['course'] != ""):

            newMenuItem = MenuItem(name = request.form['newMenuName'],
            description = request.form['description'],
            price = request.form['price'], course = request.form['course'],
                restaurant_id = restaurant.id, user_id = login_session['user_id'])
            session.add(newMenuItem)
            session.commit()
            flash("New menu item added Successfully !!")
            return redirect(url_for('showRestaurantMenu',
                restaurant_id = restaurant.id))
        else:
            flash("All fields are necessary!!")
            return render_template('newmenuitem.html', restaurant = restaurant)
    else:
        return render_template('newmenuitem.html', restaurant = restaurant)

# This module edit the menu item in the database
@app.route('/editmenuitem/<int:menu_id>/', methods = ['GET','POST'])
@login_required
def editMenuItem(menu_id):
    menuitem = session.query(MenuItem).filter_by(id = menu_id).first()
    if menuitem is None:
        return redirect(url_for('showRestaurants'))
    if menuitem.user_id != login_session['user_id']:
        return redirect(url_for('showRestaurants'))
    if request.method == 'POST':
        if (request.form['newMenuName'] != "" and
            request.form['description'] != "" and request.form['price'] != ""
            and request.form['course'] != ""):

            menuitem.name = request.form['newMenuName']
            menuitem.description = request.form['description']
            menuitem.price = request.form['price']
            menuitem.course = request.form['course']
            session.add(menuitem)
            session.commit()
            flash('Menu item edited successfully !!')
            return redirect(url_for('showRestaurantMenu',
                restaurant_id = menuitem.restaurant_id))
        else:
            flash("All fields are necessary!!")
            return render_template('editmenuitem.html', menuitem = menuitem)
    else:
        return render_template('editmenuitem.html', menuitem = menuitem)

@app.route('/deletemenuitem/<int:menu_id>/', methods=['GET','POST'])
@login_required
def deleteMenuItem(menu_id):
    menuitem = session.query(MenuItem).filter_by(id = menu_id).first()
    if menuitem is None:
        flash("Permission denied!!")
        return redirect(url_for('showRestaurants'))
    if menuitem.user_id != login_session['user_id']:
        flash("Permission denied!!")
        return redirect(url_for('showRestaurants'))
    if request.method == 'POST':
        session.delete(menuitem)
        session.commit()
        flash('Menu Item deleted successfully !!')
        return redirect(url_for('showRestaurantMenu',
            restaurant_id = menuitem.restaurant_id))
    else:
        return render_template('deletemenuitem.html', menuitem = menuitem)

# User Helper functions
def createUser(login_session):
    newUser = User(name = login_session['username'],
        email = login_session['email'], avatar = login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email = login_session['email']).one()
    return user.id

def getUserID(email):
    try:
        user = session.query(User).filter_by(email = email).one()
        return user.id
    except:
        return None

def getUserInfo(user_id):
    user = session.query(User).filter_by(id = user_id).one()
    return user

# This method generates random string state of 32 chars
@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
        for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE = state)

# This method is used to connect to google plus
@app.route('/gconnect', methods=['POST'])
def gconnect():
    '''
    gconnect: Method for logging into site using Google authentication.

    Returns:
        Renders logged in page, then redirects to home page.
    '''
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                 "Current user is already connected."), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    print "done!"
    print login_session
    return render_template("loggedin.html", login_session=login_session)

@app.route('/gdisconnect/')
def gdisconnect():
    '''
    gdisconnect: Method for logging out of site, revokes user's Google tokens.

    Returns:
        Redirects to home page.
    '''
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    # If the credentials were not found it return 401 response
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/disconnect')
def disconnect():
    '''
    disconnect: Method for logging out of site
    - This methods delete all the sessions

    Returns:
        Redirects to home page.
    '''
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        del login_session['access_token']
        del login_session['state']
        flash("You have successfully been logged out.")
        return redirect(url_for('showRestaurants'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showRestaurants'))


if __name__ == '__main__':
    # secret_key will be used for session
    app.secret_key = "hello_fsnd"
    app.run(host='0.0.0.0', port=5000, debug=True)
