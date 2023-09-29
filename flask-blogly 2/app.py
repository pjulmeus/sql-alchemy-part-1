"""Blogly application."""
from flask import Flask, request, redirect, render_template
from models import db, connect_db,  User, Post, Tag, PostTag
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
    posts = Post.query.all()
    return render_template('details.html', users = users, posts =posts)

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

@app.route("/users/<int:users_id>/posts/new")
def get_posts_form(users_id):
    u = User.query.get_or_404(users_id)
    tags = Tag.query.all()
    return render_template('add_post.html', u = u, tags = tags)


@app.route("/users/<int:users_id>/posts/new", methods = ['POST'])
def posts_form(users_id):
    u = User.query.get(users_id)
    tags = Tag.query.all()
    title = request.form['title']
    content = request.form['content'] 

    new_post = Post(title = title, content = content, user_id = users_id)
    db.session.add(new_post)
    db.session.commit()

    for t in tags: 
        tag_name = request.form.get(f"{t.id}")
        if tag_name:
            new_post_tag= PostTag(post_id = new_post.id, tag_id = t.id)
    
    db.session.add(new_post_tag)
    db.session.commit()
    return redirect (f"/users/{users_id}")

@app.route("/users/posts/<int:posts_id>")
def post(posts_id):
    u_post = Post.query.get(posts_id)
    pt = PostTag.query.filter(PostTag.post_id == posts_id).all()
    return render_template('post.html', u_post = u_post, pt= pt)

@app.route("/users/posts/<int:posts_id>/edit")
def get_edit_post(posts_id):
    tags = Tag.query.all()
    u_post = Post.query.get(posts_id)
    return render_template("edit_post.html", u_post= u_post, tags=tags)

@app.route("/users/posts/<int:posts_id>/edit", methods = ["POST"])
def edit_post(posts_id):
    u_post = Post.query.get(posts_id)
    tags = Tag.query.all()
    title = request.form["title"]
    content = request.form["content"]

    if title:
        u_post.title = title
    if content:
        u_post.content = content
    
    for t in tags: 
        tag_name = request.form.get(f"{t.id}")
        if tag_name:
            new_post_tag= PostTag(post_id = u_post.id, tag_id = t.id)
            db.session.add(new_post_tag)

    db.session.commit()
    
    return redirect(f"/users/posts/{posts_id}")

@app.route("/users/posts/<int:posts_id>/delete", methods = ["POST"])
def posts_delete(posts_id): 
    """Delete the user post and redirect to the home page """
    p_id = Post.query.get(posts_id)
    Post.query.filter(Post.id == int(posts_id)).delete()
    db.session.commit()
    return redirect("/users")


@app.route('/tags/new')
def add_tag_form():
    """GET page for User form """
    return render_template('add_tag.html')

@app.route('/tags/new', methods = ["POST"])
def post_add_tag():
    """Post request for add tag form"""
    tag_name = request.form['tag_name']

    new_tag = Tag(tag_name=tag_name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags') 

@app.route('/tags')
def tag_page():
    """List all tags in"""
    tags = Tag.query.all()
    return render_template("tags.html", tags = tags)

@app.route("/tags/<int:tags_id>/edit")
def tag_edit(tags_id):
    t = Tag.query.get(tags_id)
    return render_template("edit_post.html", t= t)

@app.route("/tags/<int:tags_id>/edit", methods = ["POST"])
def tag_edit_post(tags_id):
    t = Tag.query.get(tags_id)
    tag_name = request.form["tag_name"]

    if tag_name:
        t.tag_name = tag_name

    db.session.commit()
    
    return redirect(f"/tags/{tags_id}")

@app.route("/tags/<int:tags_id>/")
def tag_list(tags_id):
    t = Tag.query.get(tags_id)
    pt = PostTag.query.filter(PostTag.tag_id == tags_id).all()
    # v = pt.post_tags[0]
    return render_template("tag_details.html", pt=pt , t= t )