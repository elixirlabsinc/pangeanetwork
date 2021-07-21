from models.co_op import CoOpModel
from models.revolving_fund import RevolvingFundModel
from models.role import RoleModel
from models.user import UserModel
from datetime import datetime, timedelta

def create_tables(db):
    db.drop_all()
    db.create_all()
    admin_role = RoleModel('Admin', 'admin role')
    member_role = RoleModel('Member', 'member role')
    admin_role.save_to_db()
    member_role.save_to_db()

    co_op_a = CoOpModel('CoOp A', True, datetime.now(), datetime.now() + timedelta(days = 365*5), 'Seattle', 20000, 20000)
    co_op_a.save_to_db()
    admin = UserModel('Admin', 'A', 'admina@pangea.com', '+14134009988', 'admin', admin_role.id, co_op_a.id)
    admin.save_to_db()
    member = UserModel('Member', 'B', 'memberb@pangea.com', '+14134009987', 'test123', member_role.id, co_op_a.id)
    member.save_to_db()

    fund = RevolvingFundModel(2000, 2000, datetime.now(), datetime.now() + timedelta(days = 365*5), member.id)
    fund.save_to_db()

    member.revolving_fund = fund
    member.save_to_db()
