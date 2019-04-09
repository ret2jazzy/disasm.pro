from . import ninja_socketio
from .settings import get_settings
from flask import session
from .constants import capstone_modes
from capstone import *
from flask_socketio import emit

capstone_instances = {}

def init_capstone():
    global capstone_instances
    for ARCH in capstone_modes:
        current_arch = capstone_modes[ARCH]
        
        if ARCH not in capstone_instances:
            capstone_instances[ARCH] = {}

        for MODE in current_arch['MODES']:
            current_mode = current_arch['MODES'][MODE]

            if MODE not in capstone_instances[ARCH]:
                capstone_instances[ARCH][MODE] = {}

            for ENDIAN in current_mode['ENDIAN']:
                current_endian = current_mode['ENDIAN'][ENDIAN]

                capstone_instances[ARCH][MODE][ENDIAN] = Cs(current_arch['VAL'], current_mode['VAL'] + current_endian['VAL'])

@ninja_socketio.on('disassemble')
def disassemble(code):
    try:
        current_settings = get_settings() 

        current_capstone = capstone_instances[current_settings['ARCH']][current_settings['MODE']][current_settings['ENDIAN']]
        try:
            current_offset = int(current_settings['OFFSET'], 16)
        except:
            current_offset = int(current_settings['OFFSET'])

        code_to_disassemble = bytes([X for Y in code['code'] for X in Y]) #Flatten the list

        output_instructions = ""

        for instr in current_capstone.disasm(code_to_disassemble, current_offset):
            output_instructions += "{} {}\n".format(instr.mnemonic, instr.op_str)

        emit('disassembled', output_instructions)
    except Exception as e:
        print(e)
        emit('error', str(e).split("(")[0]) #Super hack to get the first part of a Keystone error message
        return



         
