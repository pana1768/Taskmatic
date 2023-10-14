import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from db.model import create_tables, Users, Tasks, GroupExecutor, AllGroup
DSN = 'postgresql://postgres:pana@localhost:5432/database'
engine = sq.create_engine(DSN)
create_tables(engine)
def make_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def register_user(user_id,name,username):
    session = make_session()
    reg = Users(user_id=user_id,name=name,username=username)
    session.add(reg)
    session.commit()
    session.close()

def add_task(task_name, task_description):
    session = make_session()
    new_task = Tasks(name_task=task_name, description_task=task_description)
    session.add(new_task)
    session.commit()
    session.close()


def user_take_task(task_id, user_id):
    session = make_session()
    take_task = session.query(Tasks).filter(Tasks.task_id == task_id).update({'user_take': user_id})
    session.commit()
    session.close()

def create_group(name,admin):
    session = make_session()
    group = AllGroup(group_name=name,admin_id=admin)
    session.add(group)
    session.commit()
    session.close()
    create_invite_id(name,admin)

def create_invite_id(group_name, admin_id):
    session = make_session()
    invite_id = ''
    for c in session.query(AllGroup).filter(AllGroup.group_name == group_name).filter(AllGroup.admin_id == admin_id):
        invite_id = c.group_name + '_' + str(c.group_id)
    update = session.query(AllGroup).filter(AllGroup.group_name == group_name).filter(AllGroup.admin_id == admin_id).update({'invite_id' : invite_id})
    session.commit()
    session.close()

# create_invite_id('sdg',481370222)

# create_group(name='newgroup',admin=222)
def get_id_group(admin_id, group_name):
    session = make_session()
    for c in session.query(AllGroup).filter(AllGroup.admin_id == admin_id).all():
        if c.group_name == group_name:
            session.close()
            return c.group_id
def check_doubled_name(admin_id, group_name):
    session = make_session()
    for c in session.query(AllGroup).filter(AllGroup.admin_id == admin_id).all():
        if c.group_name == group_name:
            session.close()
            return False
    session.close()
    return True
def check_user(user_id):
    session = make_session()
    if session.query(Users).filter(Users.user_id == user_id).all() == []:
        session.close()
        return True
    else:
        session.close()
        return False
def join_group(invite_id, user_id):
    group_name, group_id = invite_id.split('_')
    session = make_session()
    ses = 0
    for c in session.query(AllGroup).filter(AllGroup.group_id == int(group_id)).all():
        ses = c.admin_id
    new_worker = GroupExecutor(user_id=user_id,group_id=group_id,group_name=group_name,admin_id=ses)
    session.add(new_worker)
    session.commit()
    session.close()

# join_group('лопил_8',934478159)
def get_admin_groups(user_id):
    session = make_session()
    arr = []
    for c in session.query(AllGroup).filter(AllGroup.admin_id == user_id).all():
        arr.append({'Group name' : c.group_name, 'Group id' : c.group_id})
    return arr



def delete_group(invite_id):
    session = make_session()
    delete = session.query(AllGroup).filter(AllGroup.invite_id == invite_id).delete()
    session.commit()
    session.close()



def delete_member(username,group_id):
    session = make_session()
    user_id = 0
    for c in session.query(Users).filter(Users.username == username).all():
        user_id = c.user_id
    delete = session.query(GroupExecutor).filter(GroupExecutor.group_id == group_id).filter(GroupExecutor.user_id == user_id).delete()
    session.commit()
    session.close()

def info_groups():
    pass


def get_executor_group():
    pass




