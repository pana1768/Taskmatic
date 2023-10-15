import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from db.model import create_tables, Users, Tasks, GroupExecutor, AllGroup
DSN = 'postgresql://postgres:pana@localhost:5432/database'
engine = sq.create_engine(DSN)
create_tables(engine)

def save_data(file_name):
    with open(file_name, 'rb') as file:
        file_data = file.read()
    return file_data

def admin_in_processing(group_id):
    session = make_session()
    arr = []
    for c in session.query(Tasks).filter(Tasks.task_group == group_id).filter(Tasks.status_task == 'today'):
        for i in session.query(Users).filter(Users.user_id == c.user_id).all():
            username = i.username
        arr.append({'Название задачи: ':c.name_task,'Пользователь: ' : username})
    return arr

def get_free_task(group_id):
    session = make_session()
    arr = []
    for c in session.query(Tasks).filter(Tasks.task_group == group_id).filter(Tasks.status_task == 'free').all():
        arr.append({'string' : '<b>'+c.name_task+'</b>'+ '\n' + '    '+c.description_task, 'task_id' : c.task_id})
    return arr

def take_free_task(user_id,task_id):
    session = make_session()
    update = session.query(Tasks).filter(Tasks.task_id == task_id).update({'user_take':user_id, 'status_task' : 'today'})
    session.commit()
    session.close()

def get_tasts_group():
    pass

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

def add_task_user(dict_data):
    task_name = dict_data['task_name']
    task_description = dict_data['task_description']
    user_id = dict_data['user_id']
    task_group = dict_data['task_group']
    session = make_session()
    new_task = Tasks(name_task=task_name, description_task=task_description, user_take=user_id, task_group=task_group,status_task='today')
    session.add(new_task)
    session.commit()
    session.close()

# add_task_user({'task_name':'name','task_description':'description','user_id':10,'task_group':15})

def get_tasks_user(user_id):
    session = make_session()
    arr = []
    for c in session.query(Tasks).filter(Tasks.user_take == user_id).filter(Tasks.status_task == 'today').all():
        arr.append({'string' : '<b>'+c.name_task+'</b>'+ '\n' + '    '+c.description_task, 'task_id' : c.task_id})
    return arr

def send_review(task_id,review):
    session = make_session()
    new = session.query(Tasks).filter(Tasks.task_id == task_id).update({'description_task':review, 'status_task' : 'sended'})
    session.commit()
    session.close()

def add_task_admin():
    session = make_session()
    new_task = Tasks(name_task='a', description_task='aha', user_take=15, task_group=2,status_task='free')
    session.add(new_task)
    session.commit()
    session.close()

# add_task_admin()
def edit_task_user_name(task_id,new_name):
    session = make_session()
    update = session.query(Tasks).filter(Tasks.task_id == task_id).update({'name_task':new_name})
    session.commit()
    session.close()
def edit_task_user_description(task_id,new_description):
    session = make_session()
    update = session.query(Tasks).filter(Tasks.task_id == task_id).update({'description_task': new_description})
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

# join_group('lnkln_3',934478159)
def get_admin_groups(user_id):
    session = make_session()
    arr = []
    for c in session.query(AllGroup).filter(AllGroup.admin_id == user_id).all():
        arr.append({'Group name' : c.group_name, 'Group id' : c.group_id})
    if arr == []:
        return 'You haven`t group'
    else:
        return arr

def delete_group(group_id):
    session = make_session()
    delete = session.query(AllGroup).filter(AllGroup.group_id == group_id).delete()
    delete_m = session.query(GroupExecutor).filter(GroupExecutor.group_id == int(group_id)).delete()

    session.commit()
    session.close()

def delete_member(username,group_id):
    session = make_session()
    user_id = 0
    for c in session.query(Users).filter(Users.username == username).all():
        user_id = c.user_id
    res = session.query(GroupExecutor).filter(GroupExecutor.group_id == group_id).filter(GroupExecutor.user_id == user_id).delete()
    session.commit()
    session.close()
    return res

def info_groups(group_id):
    session = make_session()
    count_members = 0
    count_tasks = 0
    group_name = ''
    for c in session.query(AllGroup).filter(AllGroup.group_id == group_id).all():
        group_name = c.group_name
    for c in session.query(GroupExecutor).filter(GroupExecutor.group_id == group_id).all():
        count_members += 1
    for c in session.query(Tasks).filter(Tasks.task_group == group_id).all():
        count_tasks += 1
    result = '<b>' + group_name + '</b>' + '\n' + '    ' + 'Количество участников: ' + str(count_members) + '\n' + '    ' + 'Количество заданий: ' + str(count_tasks)
    return result

def get_executor_group(user_id):
    session = make_session()
    arr = []
    for c in session.query(GroupExecutor).filter(GroupExecutor.user_id == user_id).all():
        arr.append({'Group name' : c.group_name, 'Group id' : c.group_id})
    if arr == []:
        return []
    else:
        return arr

def leave_group(group_id,user_id):
    session = make_session()
    delete = session.query(GroupExecutor).filter(GroupExecutor.group_id == group_id).filter(GroupExecutor.user_id == user_id).delete()
    session.commit()
    session.close()
    return delete




