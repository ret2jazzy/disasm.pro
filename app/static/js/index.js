//There is some ambiguity in the js I wrote, assembled code and machine code are the same thing while disassembled code and asm code are the same thing. That'll help you understand the variable names if you want to...
const settings_skeleton = {'ARCH' : '', 'MODE' : '', 'ENDIAN' : '', 'OFFSET' : '', 'VIEW' : ''}

let global_settings = localStorage;
//The assembled code bytes are the stored code from the last set_settings
let socket, asm_editor, machine_editor;

let mutex_lock = false;
    
document.body.onload = ()=> {

    socket = io.connect('http://' + document.domain + ':' + location.port); // SocketIO's socket

    socket.on('assembled', update_assembled_code)

    socket.on('disassembled', update_disassembled_code)

    init_settings()

    //Handler for when we receive assembled code

    document.getElementById('ARCH').addEventListener('change', function(){
        arch_update(document.getElementById('ARCH').value);
        update_settings_to_server();
    })
    
    document.getElementById('MODE').addEventListener('change', function(){
        mode_update(document.getElementById('MODE').value);
        update_settings_to_server();
    })

    document.getElementById('ENDIAN').addEventListener('change', function(){
        endian_update(document.getElementById('ENDIAN').value);
        update_settings_to_server();
    })

    document.getElementById('OFFSET').addEventListener('change', function(){
        offset_update(document.getElementById('OFFSET').value);
        update_settings_to_server();
    })
    
    document.getElementById('VIEW').addEventListener('change', function(){
        view_update(document.getElementById('VIEW').value);
        update_assembled_code(JSON.parse(global_settings.machine_code_bytes));
    })

    asm_editor.session.on('change', function(delta) {
        global_settings.asm_code = asm_editor.getValue()
        if (mutex_lock) return; //A lock here is neede because setValue of ace editor fires onchange event
        send_asm_update();
    });

    machine_editor.session.on('change', function(delta) {
        global_settings.machine_code = machine_editor.getValue()
        if (mutex_lock) return;
        send_machine_update();
    });

}

function init_settings(){

    if(global_settings.ARCH === undefined){ //if only ARCH is null, aka new session, initialize everything
        default_settings = {'ARCH' : 'ARCH_X86', 'MODE' : 'MODE_64', 'ENDIAN' : 'MODE_LITTLE_ENDIAN', 'OFFSET' : '0', 'VIEW' : '1'}
        //Set the value of settings being sent to server
        for(key in default_settings){
            global_settings[key] = default_settings[key]
        }

        global_settings.asm_code = "mov rax, 0x0\n";
        global_settings.machine_code = "48 C7 C0 00 00 00 00\n"
        global_settings.machine_code_bytes = "[[0x48, 0xC7, 0xC0, 0x00, 0x00, 0x00, 0x00]]" 

    }


    asm_editor = ace.edit("asm_editor");// The editor where we write asm 
    asm_editor.setTheme("ace/theme/dawn");
    asm_editor.session.setMode("ace/mode/assembly_x86");
    asm_editor.session.setValue(global_settings.asm_code)

    machine_editor = ace.edit("machine_editor");// Where the disassebmled code is displayed
    machine_editor.setTheme("ace/theme/dawn");
    machine_editor.session.setMode("ace/mode/text");
    machine_editor.session.setValue(global_settings.machine_code)
    
    sync_settings_local()

    update_settings_to_server()

}

function update_settings_to_server(){
    current_settings = settings_skeleton;

    for (key in current_settings){
        current_settings[key] = global_settings[key]
    }

    socket.emit('update_settings', current_settings)
    //Only for when the assembler is available
    send_asm_update()
}

function clear_option_element(element){

    while (document.getElementById(element).length != 0) document.getElementById(element).remove(0);
}

function offset_update(OFFSET){
    global_settings['OFFSET'] = OFFSET;
}

function endian_update(ENDIAN){
    global_settings['ENDIAN'] = ENDIAN;
}

function mode_update(MODE){
    global_settings['MODE'] = MODE;

    current_mode = keystone_modes[global_settings['ARCH']]['MODES'][MODE]

    current_mode_endians = Object.keys(current_mode['ENDIAN'])

    clear_option_element('ENDIAN');

    current_mode_endians.forEach(function(endianness){
        let opt = document.createElement("option");
        opt.text = current_mode['ENDIAN'][endianness].DESCRIPTION
        opt.value = endianness
        document.getElementById('ENDIAN').add(opt);
    })

    if (!current_mode_endians.includes(global_settings['ENDIAN']))
        endian_update(current_mode_endians[0])
    else {
        document.getElementById('ENDIAN').value = global_settings['ENDIAN']
    }

}

function arch_update(ARCH){
    global_settings['ARCH'] = ARCH;

    current_arch = keystone_modes[ARCH]

    current_arch_modes = Object.keys(current_arch['MODES'])

    clear_option_element('MODE')

    current_arch_modes.forEach(function(mode){
        let opt = document.createElement("option");
        opt.text = current_arch['MODES'][mode].DESCRIPTION
        opt.value = mode
        document.getElementById('MODE').add(opt);
    })

    if (!current_arch_modes.includes(global_settings['MODE']))
        mode_update(current_arch_modes[0]);
    else {
        document.getElementById('MODE').value = global_settings['MODE']
    }
}

function view_update(VIEW){
    global_settings['VIEW'] = VIEW;
}

function sync_settings_local(){
    //Just change the ARCH, it will start a chain of event handlers...
    document.getElementById('ARCH').value = global_settings['ARCH']
    arch_update(global_settings['ARCH']);

    document.getElementById('MODE').value = global_settings['MODE']
    mode_update(global_settings['MODE']);

    document.getElementById('ENDIAN').value = global_settings['ENDIAN']
    endian_update(global_settings['ENDIAN']);

    document.getElementById('OFFSET').value = global_settings['OFFSET']
    offset_update(global_settings['OFFSET']);

    document.getElementById('VIEW').value = global_settings['VIEW']
    view_update(global_settings['VIEW']);
}

