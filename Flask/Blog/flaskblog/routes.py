#!/usr/bin/env python3

import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegisterationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'Author 1',
        'title': 'Post 1',
        'content': 'First post',
        'date_posted': 'December 26, 2019'
    },
    {
        'author': 'Author 2',
        'title': 'Post 2',
        'content': 'Second post',
        'date_posted': 'January 3, 2020'
    }
]

@app.route('/')
@app.route('/home')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title="About")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('home')
    
    form = RegisterationForm()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f"Account created for {form.username.data}!", category="success")
        
        return redirect(url_for('login'))
    
    return render_template('register.html', title="Register", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('home')
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            
            next_page = request.args.get('next')
            
            return redirect(next_page) if next_page else redirect('home')
        else:
            flash("Incorrect Username or Password!", category="danger")
    
    return render_template('login.html', title="Login", form=form)

@app.route('/logout')
def logout():
    logout_user()
    
    return redirect('home')

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            random_hex = secrets.token_hex(8)
            _,f_ext = os.path.splitext(form.picture.data.filename)
            picture_fn = random_hex + f_ext
            picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)

            i = Image.open(form.picture.data)
            i.thumbnail((125, 125))
            
            i.save(picture_path)
            
            current_user.image = picture_fn
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        
        flash("Your account has been updated!", "success")
        
        return redirect(url_for('account'))
    
    form.username.data = current_user.username
    form.email.data = current_user.email
    
    return render_template('account.html', title="Account", form=form)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        
        db.session.add(post)
        db.session.commit()
        
        flash("Your post has been created!", "success")
        
        return redirect(url_for('about'))
    
    return render_template("create_post.html", title="New Post", form=form)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post_id))
    form.title.data = post.title
    form.content.data = post.content
    return render_template("create_post.html", title="Update Post", form=form)

@app.route('/post/<int:post_id>/delete')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('about'))