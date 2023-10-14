import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship
# from sqlalchemy import Table, Column, Integer, String, MetaData

# meta_obj = MetaData()
Base = declarative_base()

class Users(Base):
    __tablename__ = 'registered_users'

    user_id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String)
    # groups = sq.Column(sq.Integer,sq.ForeignKey())


    def __str__(self):
        return f'{self.user_id}: {self.name}'


class Tasks(Base):
    __tablename__ = 'tasks'

    task_id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    name_task = sq.Column(sq.String(length=40))
    description_task = sq.Column(sq.String(length=1000))
    user_take = sq.Column(sq.Integer)

    # user = relationship(Users, backref='task')
    def __str__(self):
        return f'{self.task_id} : {self.name_task} : {self.description_task}'

class AllGroup(Base):
    __tablename__ = 'all_group'

    group_id = sq.Column(sq.Integer,primary_key=True)
    group_name = sq.Column(sq.String, unique=True)
    admin_id = sq.Column(sq.Integer, unique=True)
    # user_id = sq.Column(sq.Integer, )

    # users = relationship(Users, backref=)

class GroupExecutor(Base):
    __tablename__ = 'group_executor'

    user_id = sq.Column(sq.Integer,primary_key=True)
    group_id = sq.Column(sq.Integer)
    group_name = sq.Column(sq.String)

    # user = relationship(Users, backref='groupcutor')
def create_tables(engine):
    Base.metadata.create_all(engine)




