"""Blogly application."""
from flask import Flask, request, redirect, render_template
from models import db, connect_db,  User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

# @app.route('/')
# def testing():
#     return render_template("base.html")

@app.route('/users')
def list_user_page():
    """List all user in, Users Object"""
    users = User.query.all()
    return render_template("home.html", users = users)

@app.route('/users/new')
def user_form():
    """GET page for User form """
    return render_template('adduser.html')

@app.route('/users/new', methods = ["POST"])
def user_detail_page():
    """Post request for User Form"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_users = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_users)
    db.session.commit()

    return redirect('/users') 

@app.route("/users/<int:users_id>")
def users_form(users_id):
    """User detail page"""
    users = User.query.get_or_404(users_id)
    return render_template('details.html', users = users)

@app.route("/users/<int:users_id>/delete", methods = ["POST"])
def users_delete(users_id): 
    """Delete the user post and redirect to the home page """
    print(users_id)
    User.query.filter(User.id == int(users_id)).delete()
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:users_id>/edit')
def user_edit(users_id):
    """User Edit Page"""
    u = User.query.get_or_404(users_id)
    return render_template('edit_page.html', u = u)

@app.route("/users/<int:users_id>/edit", methods = ["POST"])
def users_form2(users_id): 
    print(users_id)
    u = User.query.get(users_id)
    print(u)
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    
    if first_name:
        u.first_name = first_name
    if last_name:
        u.last_name = last_name
    if image_url:
        u.image_url = image_url

    db.session.commit()

    return redirect(f"/users/{users_id}")




