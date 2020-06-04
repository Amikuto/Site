# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 10:27:22 2020

@author: damir
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some_secret_pass'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    # SQLALCHEMY_TRACK_MODIFICATIONS = False
