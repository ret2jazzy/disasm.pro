from flask import session
from flask_socketio import emit
from . import ninja_socketio
from .settings import get_settings
from .constants import keystone_modes
from .disassemble import capstone_instances
from keystone import *

keystone_instances = {}

#Initialize all the keystone instances so we can access them directly based on values in the settings
# def init_keystone():
    # global keystone_instances
    # keystone_instances = {}

    # for ARCH in keystone_modes:
        # current_arch = keystone_modes[ARCH]
        
        # if ARCH not in keystone_instances:
            # keystone_instances[ARCH] = {}

        # for MODE in current_arch['MODES']:
            # current_mode = current_arch['MODES'][MODE]

            # if MODE not in keystone_instances[ARCH]:
                # keystone_instances[ARCH][MODE] = {}

            # for ENDIAN in current_mode['ENDIAN']:
                # current_endian = current_mode['ENDIAN'][ENDIAN]

                # keystone_instances[ARCH][MODE][ENDIAN] = Ks(current_arch['VAL'], current_mode['VAL'] + current_endian['VAL'])
                

"""
Receive a JSON Object with data to assemble
"""

@ninja_socketio.on('assemble')
def assemble(code):
    try:
        current_settings = get_settings()
        
        try:
            starting_offset = int(current_settings['OFFSET'], 16)
        except:
            starting_offset = int(current_settings['OFFSET'])
        current_offset = starting_offset 

        #We are gonna do an hack to support labels, since I want line by line assembly and also support labels
        #And labels won't work if we assemble it line by line cuz labels will be on a different lien
        #So, I'm gonna first assemble it all at once, and then assemble each line, catching any symbol exceptions for labels
        #I'll then disassemble the originally assembled code code at that point to get the the instruction that uses the label and add it

        current_arch = keystone_modes[current_settings['ARCH']]
        current_mode = current_arch['MODES'][current_settings['MODE']]
        current_endian = current_mode['ENDIAN'][current_settings['ENDIAN']]

        current_keystone = Ks(current_arch['VAL'], current_mode['VAL']+current_endian['VAL'])
        assembled_code = current_keystone.asm_new(code['code'],current_offset)[0] 

        emit('assembled', assembled_code)
    except Exception as e:
        print(e)
        emit('error', str(e).split("(")[0]) #Super hack to get the first part of a Keystone error message
        return
