from models import db

class RevolvingFundModel(db.Model):
    __tablename__ = 'revolving_funds'

    id = db.Column(db.Integer, primary_key=True)
    initial_balance = db.Column(db.Integer)
    balance = db.Column(db.Integer)
    interest = db.Column(db.Integer)
    loan_start = db.Column(db.DateTime)
    loan_end = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, initial_balance, balance, loan_start, loan_end, user_id):
        self.initial_balance = initial_balance
        self.balance = balance
        self.loan_start = loan_start
        self.loan_end = loan_end
        self.user_id = user_id

    def json(self):
        return {
            'id': self.id,
            'initial_balance': self.initial_balance,
            'balance': self.balance,
            'loan_start': '', #self.loan_start,
            'loan_end': '', #self.loan_end,
            'user': self.user.first_name + ' ' + self.user.last_name
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
