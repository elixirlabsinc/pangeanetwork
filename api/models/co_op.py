from models import db

class CoOpModel(db.Model):
  __tablename__ = 'co_ops'

  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), unique=True)
  is_active = db.Column(db.Boolean())
  start_date = db.Column(db.DateTime())
  end_date = db.Column(db.DateTime())
  location = db.Column(db.String(255))
  initial_balance = db.Column(db.Integer())
  current_balance = db.Column(db.Integer())
  users = db.relationship('UserModel', uselist=False, backref='co_op')

  def __init__(self, name, is_active, start_date, end_date, location, initial_balance, current_balance):
      self.name = name
      self.is_active = is_active
      self.start_date = start_date
      self.end_date = end_date
      self.location = location
      self.initial_balance = initial_balance
      self.current_balance = current_balance

  def json(self):
      return {
          'id': self.id,
          'name': self.name,
          'is_active': self.is_active,
          'start_date': '', #self.start_date,
          'end_date': '', #self.end_date,
          'location': self.location,
          'initial_balance': self.initial_balance,
          'current_balance': self.current_balance
      }
    
  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def find_by_co_op_id(cls, _id):
    return cls.query.filter_by(id=_id).first()
