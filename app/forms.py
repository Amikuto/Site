# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 10:45:40 2020

@author: damir
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Train
from app import db


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    full_name = StringField('Ваши ФИО', validators=[DataRequired()])
    username = StringField('Имя пользователя', validators=[DataRequired()])  # TODO: End full name (add to db etc)
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегестрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другое имя.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другой email.')


class AcceptForm(FlaskForm):
    submit = SubmitField('На главную страницу')


class TrainSetForm(FlaskForm):
    city_dep = StringField('Город отправления (Краснодар)', validators=[DataRequired()])
    city_arr = StringField('Город прибытия (Москва)', validators=[DataRequired()])
    date_dep = StringField('Дата отправления (01.01.01)', validators=[DataRequired()])
    time_dep = StringField('Время отправления (12:12)', validators=[DataRequired()])
    date_arr = StringField('Дата прибытия (01.01.01)', validators=[DataRequired()])
    time_arr = StringField('Время прибытия (12:12)', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class TrainDeleteForm(FlaskForm):
    id = IntegerField('Введите id поезда', validators=[DataRequired()])
    submit = SubmitField('Удалить')


class TicketSetForm(FlaskForm):
    cost = StringField('Стоимость', validators=[DataRequired()])
    train_number = StringField('Номер поезда', validators=[DataRequired()])
    owner = StringField('Владелец (id)')
    submit = SubmitField('Добавить')


class PayCommitForm(FlaskForm):
    submit = SubmitField('На главную страницу')


class BuyTicketForm(FlaskForm):
    tickets = StringField('Номер билета', validators=[DataRequired()])
    email = StringField('Email на который будут высланы билеты и способы оплаты:', validators=[DataRequired(), Email()])
    submit = SubmitField('Далее')


class SecondBuyTicketForm(FlaskForm):
    city_dep = SelectField('Город отправления', choices=[(i.city_dep, i.city_dep) for i in Train.query.order_by(Train.id).all()])
    city_arr = SelectField('Город прибытия', choices=[(i.city_arr, i.city_arr) for i in Train.query.order_by(Train.id).all()])
    date = StringField('Дата отправления (01.01.01)')
    submit = SubmitField('Поиск')


class EditProfileForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Изменить')
