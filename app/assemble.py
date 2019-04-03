from flask import session
from . import ninja_socketio
from .constants import keystone_modes
from keystone import *

keystone_instances = {}

#Initialize all the keystone instances so we can access them directly based on values in the settings
def init_keystone():
    global keystone_instances
    keystone_instances = {}

    for ARCH in keystone_modes:
        current_arch = keystone_modes[ARCH]
        
        if ARCH not in keystone_instances:
            keystone_instances[ARCH] = {}

        for MODE in current_arch['MODES']:
            current_mode = current_arch['MODES'][MODE]

            if MODE not in keystone_instances[ARCH]:
                keystone_instances[ARCH][MODE] = {}

            for ENDIAN in current_mode['ENDIAN']:
                current_endian = current_mode['ENDIAN'][ENDIAN]

                keystone_instances[ARCH][MODE][ENDIAN] = Ks(current_arch['VAL'], current_mode['VAL'] + current_endian['VAL'])
                

"""
Receive a JSON Object with data to assemble
"""

@ninja_socketio.on('assemble')
def assemble(code):
    print("Assembling", code['code'])
    try:
        current_settings = session['settings']

        current_keystone = keystone_instances[current_settings['ARCH']][current_settings['MODE']][current_settings['ENDIAN']]

        code_to_assemble = code['code'].strip().split("\n")

        assembled_code = []

        current_offset = current_settings['OFFSET']

        for each_line in code_to_assemble:
            machine_line = current_keystone.asm(each_line,  int(current_offset))[0]
            if machine_line is None:
                machine_line = []
            assembled_code.append(machine_line)

        ninja_socketio.emit('assembled', assembled_code)
    except:
        print("error assembling")
        return 
