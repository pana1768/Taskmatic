from telebot.handler_backends import State, StatesGroup


class Groups(StatesGroup):
    choosertype = State()
    manager = State()
    executor = State()
    chooserole = State()
    edit = State()
    view = State()
    chooseactionadmin = State()
    editgroup = State()
    edit = State()
    wait_username = State()
    
class Tasks(StatesGroup):
    chooserole = State()

class CreateGroup(StatesGroup):
    entername = State()
    
class RandomStates(StatesGroup):
    chooseaction = State()
    register = State()
    start_work = State()
    wait_invite_link = State()
    chose_leave = State()
    
    
    
class Tasks(StatesGroup):
    choserole = State()
    choseactionmember = State()
    creating = State()
    name = State()
    description = State()
    wait = State()
    choosechange = State()
    changename = State()
    changedesc = State()
    createreview = State() 
    choseactionadmin = State()
    adminprocess = State()
    