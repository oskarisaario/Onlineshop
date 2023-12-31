from flask import render_template, session, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError

from application import app, db, bcrypt
from application.products.models import Addproduct, Brand, Category
from .forms import RegistrationForm, LoginForm
from .models import User

import os

#################### Routes for admin site ####################

#################### View all products(edit/delete) ####################
@app.route("/admin")
def admin():
    if 'username' not in session:
        flash('Login required, please login first', 'danger')
        return redirect(url_for('adminLogin'))
    products = Addproduct.query.all()
    return render_template('admin/index.html', title='Admin page', products=products)


#################### View brands(edit/delete) ####################
@app.route('/brands')
def brands():
    if 'username' not in session:
        flash('Login required, please login first', 'danger')
        return redirect(url_for('adminLogin'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title="Brand page", brands=brands)


#################### View category(edit/delete) ####################
@app.route('/category')
def category():
    if 'username' not in session:
        flash('Login required, please login first', 'danger')
        return redirect(url_for('adminLogin'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html', title="Brand page", categories=categories)


#################### Register for admin site ####################
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user = User(name = form.name.data, username = form.username.data, email=form.email.data, password = hash_password)
        db.session.add(user)
        db.session.commit()
        flash('Registered succesfully, please login', 'success')
        return redirect(url_for('adminLogin'))
    return render_template('admin/register.html', form=form, title="Registration Page")


#################### login for admin site ####################
@app.route('/login', methods=['GET', 'POST'])
def adminLogin():
    form =LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['username'] = form.username.data
            flash(f'Logged in as {form.username.data}', 'success')
            return redirect(request.args.get('next') or url_for('admin'))

        flash('Invalid password, please try again', 'danger')
    return render_template('admin/login.html', form=form, title="Login Page")


@app.route('/logout', methods=['GET', 'POST'])
def adminLogout():
    session['username'] = None
    return redirect(url_for('adminLogin'))