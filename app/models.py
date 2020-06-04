# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 12:40:13 2020

@author: damir
"""

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    tickets = db.relationship('Ticket', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)



class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Integer, index=True)
    train_id = db.Column(db.Integer, db.ForeignKey('train.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'Билет {} | стоимость: {}  поезд: {}'.format(self.id, self.cost, self.train_id)


class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_arr = db.Column(db.String(120), index=True)
    date_dep = db.Column(db.String(120), index=True)
    time_arr = db.Column(db.String(120), index=True)
    time_dep = db.Column(db.String(120), index=True)
    city_arr = db.Column(db.String(120), index=True)
    city_dep = db.Column(db.String(120), index=True)
    tickets = db.relationship('Ticket', backref='train_number', lazy='dynamic')

    def __repr__(self):
        return 'Поезд под номером {} | время прибытия: {} | время отправления: {} | ' \
               'город прибытия: {} | город отправления: {} | билеты: {}'.format(self.id, self.time_arr, self.time_dep,
                                                                         self.city_arr, self.city_dep, self.tickets.all())


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
