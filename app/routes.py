# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 16:53:44 2020

@author: damir
"""

from flask import render_template, flash, redirect, url_for
from app import app
from app import db
from app.forms import *
from app.models import Train, Ticket, User
from flask_login import current_user, login_user, login_required, logout_user
from flask import request
from werkzeug.urls import url_parse


# def ticket_add_to_db():
#     form = BuyTicketForm()
#     if form.validate_on_submit():
#         ticket = Ticket.query.get(form.tickets.data)
#         try:
#             if ticket.owner:
#                 flash('Билет уже куплен')
#                 return redirect(url_for('tickets'))
#             else:
#                 email = request.form.get('email')
#                 ticket.owner = User.query.get(current_user.get_id())
#                 db.session.commit()
#                 return redirect(url_for('buy', email=email))
#         except:
#             flash('Такого билета не существует!')
#             return redirect(url_for('tickets'))


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title='Домашняя страница')


@app.route('/tickets', methods=['GET', 'POST'])
@login_required
def tickets():
    form = BuyTicketForm()
    form_two = SecondBuyTicketForm()
    data = Train.query.order_by(Train.id).all()
    owner = Ticket.query.all()
    if form_two.validate_on_submit():
        return redirect(url_for('sorted_page', city_dep=form_two.city_dep.data, city_arr=form_two.city_arr.data,
                                date=form_two.date.data))
    if form.validate_on_submit():
        ticket = Ticket.query.get(form.tickets.data)
        try:
            if ticket.owner:
                flash('Билет уже куплен')
                return redirect(url_for('tickets'))
            else:
                email = request.form.get('email')
                ticket.owner = User.query.get(current_user.get_id())
                db.session.commit()
                return redirect(url_for('buy', email=email))
        except:
            flash('Такого билета не существует!')
            return redirect(url_for('tickets'))
    return render_template('tickets.html', title='Покупка билетов', form=form, form_two=form_two, data=data, owner=owner)


@app.route('/sorted', methods=['GET', 'POST'])
@login_required
def sorted_page():
    form = BuyTicketForm()
    data = Train.query.order_by(Train.id).all()
    owner = Ticket.query.all()
    city_dep = request.args.get('city_dep', None)
    city_arr = request.args.get('city_arr', None)
    date = request.args.get('date', None)
    if form.validate_on_submit():
        ticket = Ticket.query.get(form.tickets.data)
        try:
            if ticket.owner:
                flash('Билет уже куплен')
                return redirect(url_for('tickets'))
            else:
                email = request.form.get('email')
                ticket.owner = User.query.get(current_user.get_id())
                db.session.commit()
                return redirect(url_for('buy', email=email))
        except:
            flash('Такого билета не существует!')
            return redirect(url_for('tickets'))
    return render_template('sorted.html', city_dep=city_dep, city_arr=city_arr, date=date, data=data, owner=owner, form=form)


@app.route('/buy', methods=['GET', 'POST'])
def buy():
    form = PayCommitForm()
    email = request.args.get('email', None)
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('buy.html', title='Подтверждено', form=form, email=email)


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    tickets_data = Ticket.query.all()
    train_data = Train.query.order_by(Train.id).all()
    user_data = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', title='Личный кабинет', train_data=train_data, tickets_data=tickets_data,
                           user_data=user_data)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Изменения сохранены.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_profile.html', title='Редактирование данных', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильное имя пользователя или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарешестрированы!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/train_add', methods=['GET', 'POST'])
def add_trains():
    form = TrainSetForm()
    admin_list = [4, 5]
    if int(current_user.get_id()) in admin_list:
        if form.validate_on_submit():
            data = Train(time_arr=form.time_arr.data, time_dep=form.time_dep.data, city_arr=form.city_arr.data,
                         city_dep=form.city_dep.data, date_arr=form.date_arr.data, date_dep=form.date_dep.data)
            db.session.add(data)
            db.session.commit()
            return redirect(url_for('add_trains'))
    else:
        return redirect(url_for('tickets'))
    return render_template('admin_panel_train.html', title='Новый маршрут', form=form)


@app.route('/train_delete', methods=['GET', 'POST'])
def delete_trains():
    form = TrainDeleteForm()
    admin_list = [4, 5]
    if int(current_user.get_id()) in admin_list:
        if form.validate_on_submit():
            data = Train.query.filter_by(id=form.id.data).first()
            tickets_data = Ticket.query.filter_by(train_id=form.id.data).all()
            for i in tickets_data:
                db.session.delete(i)
            db.session.delete(data)
            db.session.commit()
            return redirect(url_for('delete_trains'))
    return render_template('admin_panel_delete.html', title='Новый маршрут', form=form)


@app.route('/ticket_add', methods=['GET', 'POST'])
def add_tickets():
    form = TicketSetForm()
    admin_list = [1, 4]
    if int(current_user.get_id()) in admin_list:
        if form.validate_on_submit():
            if Train.query.get(form.train_number.data):
                data = Ticket(cost=form.cost.data, train_id=form.train_number.data, user_id=form.owner.data)
                db.session.add(data)
                db.session.commit()
                return redirect(url_for('add_tickets'))
            else:
                flash('Такого поезда не существует!')
                return redirect(url_for('add_tickets'))
    else:
        return redirect(url_for('tickets'))
    return render_template('admin_panel_ticket.html', title='Новый маршрут', form=form)


@app.route('/404', methods=['GET', 'POST'])
def error():
    return render_template('404.html', title='404')
