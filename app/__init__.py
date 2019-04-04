from flask import Flask, session
from flask_socketio import SocketIO
from flask_session import Session

asm_ninja = Flask(__name__) #The main flask object

#Config settings
asm_ninja.config['SECRET_KEY'] = 'topsecrethacker'
asm_ninja.config['SESSION_TYPE'] = 'filesystem'

Session(asm_ninja)
ninja_socketio = SocketIO(asm_ninja, manage_session=False) #The socketIO app

from . import index, assemble, disassemble, settings
#Init the keystones
assemble.init_keystone()
disassemble.init_capstone()
