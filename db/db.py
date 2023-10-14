import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from db.model import create_tables, Users
DSN = 'postgresql://postgres:pana@localhost:5432/database'
engine = sq.create_engine(DSN)
create_tables(engine)
def make_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def register_user(user_id,name):
    session = make_session()
    reg = Users(user_id=user_id,name=name)
    session.add(reg)
    session.commit()
    session.close()

# def add_task(task_name, task_description):
#     session = make_session()
#     new_task = Tasks(name_task=task_name, description_task=task_description)
#     session.add(new_task)
#     session.commit()
#     session.close()
#
# def user_take_task(task_id, user_id):
#     session = make_session()
#     take_task = session.query(Tasks).filter(Tasks.task_id == task_id).update({'user_take': user_id})
#     session.commit()
#     session.close()
#
# def create_group(name,admin):
#     session = make_session()
#     group = AllGroup(group_name=name,admin_id=admin)
#     session.add(group)
#     session.commit()
#     session.close()

def check_user(user_id):
    session = make_session()
    if session.query(Users).filter(Users.user_id == user_id).all() == []:
        session.close()
        return True
    else:
        session.close()
        return False


def add_executor(user_id,group_id):
    pass




