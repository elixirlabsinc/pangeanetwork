from datetime import datetime
import json
import os
from app import db

# Models
roles_users = db.Table(
  'roles_users',
  db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
  db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

co_ops_users = db.Table(
  'co_ops_users',
  db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
  db.Column('co_op_id', db.Integer(), db.ForeignKey('co_op.id'))
)

loans_users = db.Table(
  'loans_users',
  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('loan_id', db.Integer, db.ForeignKey('loan.id'))
)

transactions_loans = db.Table(
  'transactions_loans',
  db.Column('transaction_id', db.Integer, db.ForeignKey('transaction.id')),
  db.Column('loan_id', db.Integer, db.ForeignKey('loan.id'))
)

transactions_users = db.Table(
  'transactions_users',
  db.Column('transaction_id', db.Integer, db.ForeignKey('transaction.id')),
  db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)


class CoOp(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), unique=True)
  is_active = db.Column(db.Boolean())
  start_date = db.Column(db.DateTime())
  end_date = db.Column(db.DateTime())
  location = db.Column(db.String(255))
  interest = db.Column(db.Integer())
  initial_balance = db.Column(db.Integer())
  expected_repayment = db.Column(db.Integer())
  current_balance = db.Column(db.Integer())
  users = db.relationship('User', uselist=False, backref='co_op')

  def __str__(self):
    return self.name


class Role(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), unique=True)
  description = db.Column(db.String(255))
  users = db.relationship('User', uselist=False, backref='role')

  def __str__(self):
    return self.name


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(255))
  last_name = db.Column(db.String(255))
  email = db.Column(db.String(255), unique=True)
  phone = db.Column(db.String(255), unique=True)
  password = db.Column(db.String(255))
  active = db.Column(db.Boolean())
  confirmed_at = db.Column(db.DateTime())
  co_op_id = db.Column(db.Integer, db.ForeignKey('co_op.id'))
  role_id = db.Column('Role', db.ForeignKey('role.id'))
  loan = db.relationship('Loan', uselist=False, backref='user')
  transactions = db.relationship('Transaction', secondary=transactions_users,
                                 backref='users', lazy='dynamic')

  def __str__(self):
    return self.email


class Loan(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  initial_balance = db.Column(db.Integer)
  balance = db.Column(db.Integer)
  interest = db.Column(db.Integer)
  loan_start = db.Column(db.DateTime)
  loan_end = db.Column(db.DateTime)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Transaction(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  amount = db.Column(db.Integer)
  previous_balance = db.Column(db.Integer)
  new_balance = db.Column(db.Integer)
  state = db.Column(db.String(255))
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  loan = db.relationship('Loan', secondary=transactions_loans,
                         backref=db.backref('transactions', lazy='dynamic'))

