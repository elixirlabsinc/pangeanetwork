from models import db
from datetime import datetime

class TransactionModel(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    previous_balance = db.Column(db.Integer)
    new_balance = db.Column(db.Integer)
    state = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    revolving_fund_id = db.Column(db.Integer, db.ForeignKey('revolving_funds.id'))

    def __init__(self, amount, previous_balance, new_balance, state, timestamp, user_id, revolving_fund_id):
        self.amount = amount
        self.previous_balance = previous_balance
        self.new_balance = new_balance
        self.state = state
        self.timestamp = timestamp
        self.user_id = user_id
        self.revolving_fund_id = revolving_fund_id

    def json(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'previous_balance': self.previous_balance,
            'new_balance': self.new_balance,
            'state': self.state,
            'timestamp': '', #self.timestamp,
            'user': self.user_id,
            'revolving_fund_id': self.revolving_fund_id
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
