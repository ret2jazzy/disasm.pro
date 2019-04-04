from . import ninja_socketio
from flask import session
from .constants import capstone_modes
from capstone import *

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
    current_settings = session['settings']

    current_capstone = capstone_instances[current_settings['ARCH']][current_settings['MODE']][current_settings['ENDIAN']]

    if code['view'] == '1':
        code_to_disassemble =  bytes.fromhex(code['code'].replace("\n", "").replace(" ", ""))
    else:
        code_to_disassemble = code['code'].encode().decode('unicode_escape').encode() #I love python3 /s

    output_instructions = ""

    for instr in current_capstone.disasm(code_to_disassemble, int(current_settings['OFFSET'])):
        output_instructions += "{} {}\n".format(instr.mnemonic, instr.op_str)

    ninja_socketio.emit('disassembled', output_instructions)



         
