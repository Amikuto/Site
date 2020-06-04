# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 16:54:58 2020

@author: damir
"""

from app import app, db
from app.models import User, Train, Ticket


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Train': Train, 'Ticket': Ticket}
