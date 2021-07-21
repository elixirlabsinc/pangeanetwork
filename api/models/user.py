from models import db
from models.role import RoleModel

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    password = db.Column(db.String(80))
    email = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    co_op_id = db.Column(db.Integer, db.ForeignKey('co_ops.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    revolving_fund = db.relationship("RevolvingFundModel", backref="user", uselist=False)
    transactions = db.relationship('TransactionModel', uselist=False, backref='user')


    def __init__(self, first_name, last_name, email, phone, password, role_id, co_op_id=None, revolving_fund=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.password = password
        self.role_id = role_id
        self.co_op_id = co_op_id if co_op_id else None
        self.revolving_fund = revolving_fund if revolving_fund else None


    def json(self):
        return {
            'id': self.id,
            'name': self.first_name + ' ' + self.last_name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role.name,
            'co_op': self.co_op.name if self.co_op else 'N/A',
            'revolving_fund_balance': self.revolving_fund.balance if self.revolving_fund else 'N/A'
        }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_phone(cls, phone):
        return cls.query.filter_by(phone=str(phone)).first()

    @classmethod
    def find_by_member_and_co_op_id(cls, member_id, co_op_id):
        return cls.query.filter_by(co_op_id = co_op_id, id = member_id).first()

    @classmethod
    def find_all_members_by_co_op(cls, co_op_id):
        return cls.query.filter_by(co_op_id = co_op_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
