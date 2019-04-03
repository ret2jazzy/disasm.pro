from flask import session
from  .constants import keystone_modes
from . import ninja_socketio
from keystone import *
import copy
from flask_socketio import emit


#This is basically the management of user's assembler/disassemblers config options

#New update from client
@ninja_socketio.on('update_settings')
def update(options):
    try:
        ks_ARCH = keystone_modes[options['ARCH']]
        ks_MODE = ks_ARCH['MODES'][options['MODE']]
        ks_ENDIAN = ks_MODE['ENDIAN'][options['ENDIAN']]

        session['settings'] = copy.copy(options)

    except:
        return False

@ninja_socketio.on('get_settings')
def get_settings():
    if 'settings' not in session:
        session['settings'] = {'ARCH' : 'ARCH_X86', 'MODE' : 'MODE_64', 'ENDIAN' : 'MODE_LITTLE_ENDIAN', 'OFFSET' : 0}

    emit('set_settings', session['settings'])
