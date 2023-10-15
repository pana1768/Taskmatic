import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship
# from sqlalchemy import Table, Column, Integer, String, MetaData

# meta_obj = MetaData()
Base = declarative_base()

class Users(Base):
    __tablename__ = 'registered_users'

    user_id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String)
    username = sq.Column(sq.String)
    # groups = sq.Column(sq.Integer,sq.ForeignKey())

    def __init__(self,user_id,name, username):
        self.user_id = user_id
        self.name = name
        self.username = username



    def __str__(self):
        return f'{self.user_id}: {self.name}'


class Tasks(Base):
    __tablename__ = 'tasks'

    task_id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    name_task = sq.Column(sq.String(length=40))
    description_task = sq.Column(sq.String(length=1000))
    user_take = sq.Column(sq.Integer)
    status_task = sq.Column(sq.String)
    task_group = sq.Column(sq.Integer)
    time = sq.Column(sq.DateTime(timezone=True),server_default=sq.func.now())
    # data = sq.Column(sq.bytea)

    def __init__(self,name_task,description_task, user_take, task_group, status_task):
        self.name_task = name_task
        self.description_task = description_task
        self.user_take = user_take
        self.task_group = task_group
        self.status_task = status_task

    # user = relationship(Users, backref='task')
    def __str__(self):
        return f'{self.task_id} : {self.name_task} : {self.description_task}'

class AllGroup(Base):
    __tablename__ = 'all_group'

    group_id = sq.Column(sq.Integer,primary_key=True)
    group_name = sq.Column(sq.String)
    admin_id = sq.Column(sq.Integer)
    invite_id = sq.Column(sq.String)
    # user_id = sq.Column(sq.Integer, )

    def __init__(self, group_name, admin_id):
        self.group_name = group_name
        self.admin_id = admin_id

    def __str__(self):
        return f'{self.group_id} : {self.group_name} : {self.admin_id} : {self.invite_id}'

    # users = relationship(Users, backref=)

class GroupExecutor(Base):
    __tablename__ = 'group_executor'

    admin_id = sq.Column(sq.Integer)
    user_id = sq.Column(sq.Integer,primary_key=True)
    group_id = sq.Column(sq.Integer)
    group_name = sq.Column(sq.String)

    def __init__(self,user_id,group_id,group_name, admin_id):
        self.user_id = user_id
        self.group_id = group_id
        self.group_name = group_name
        self.admin_id = admin_id

    # user = relationship(Users, backref='groupcutor')
def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)




