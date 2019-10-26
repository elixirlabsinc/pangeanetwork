from flask import Flask, request, current_app
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256 as sha256
import os
from config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
  app = Flask(__name__)
  CORS(app)
  app.config.from_object(config_class)
  app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI']

  db.init_app(app)
  app_dir = os.path.realpath(os.path.dirname(__file__))
  database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
  if not os.path.exists(database_path):
    build_sample_db(app)
  return app

from app import models


def build_sample_db(app):
  """
  Populate a small db with some example entries.
  """

  import string
  import random
  from app.models import User, CoOp, Role, Loan, Transaction 


  with app.app_context():
    db.drop_all()
    db.create_all()

    user_role = Role(name='member')
    super_user_role = Role(name='officer')
    db.session.add(user_role)
    db.session.add(super_user_role)
    db.session.commit()

    co_op_1 = CoOp(
      name='ABC',
      is_active=True,
      location='Seattle',
      interest=5,
      initial_balance=2000,
      expected_repayment=2200,
      current_balance=1500
    )

    co_op_2 = CoOp(
      name='DEF',
      is_active=True,
      location='New York',
      interest=5,
      initial_balance=4000,
      expected_repayment=4400,
      current_balance=35000
    )

    db.session.add(co_op_1)
    db.session.add(co_op_2)
    db.session.commit()

    admin_user = User(
      first_name='Admin',
      last_name='User',
      email='admin',
      password=sha256.hash('admin'),
      phone='254798745678',
      role_id=super_user_role.id,
      co_op_id=co_op_1.id
    )
    test_user = User(
      first_name='Test',
      last_name='User',
      email='test@user.com',
      password=sha256.hash('12345'),
      phone='254987654321',
      role_id=user_role.id,
      co_op_id=co_op_1.id
    )
    db.session.add(admin_user)
    db.session.add(test_user)
    db.session.commit()

    test_user_loan = Loan(
      user=test_user,
      initial_balance=2000,
      balance=2000,
      interest=2,
    )
    db.session.add(test_user_loan)
    db.session.commit()

  return
