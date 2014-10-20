# -*- coding: utf-8 -*-
from . import org
from ..models import User
from flask.ext.login import login_user
from flask import redirect, url_for, render_template, flash, request


@org.route('/login', methods=['POST'])
def login():
    return render_template('auth/login.html')


@org.route('/register', methods=['GET'])
def register():
    return render_template('organ_regiter_py.html')
