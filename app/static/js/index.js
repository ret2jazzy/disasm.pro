

let global_settings = {
    'ARCH' : null,
    'ENDIAN' : null,
    'MODE' : null,
    'OFFSET' : null,
};

let socket = io.connect('http://' + document.domain + ':' + location.port); // SocketIO's socket

let mutex_lock = false;
    
let asm_editor = ace.edit("asm_editor");// The editor where we write asm 

let machine_editor = ace.edit("machine_editor");// Where the disassebmled code is displayed

document.body.onload = ()=>{

    asm_editor.setTheme("ace/theme/dawn");
    asm_editor.session.setMode("ace/mode/assembly_x86");


    machine_editor.setTheme("ace/theme/dawn");
    machine_editor.session.setMode("ace/mode/text");

    //Handler for set_settings
    socket.on('set_settings', handle_set_settings)

    //Handler for when we receive assembled code
    socket.on('assembled', update_assembled_code)

    document.getElementById('ARCH').addEventListener('change', function(){
        arch_update(document.getElementById('ARCH').value);
    })
    
    document.getElementById('MODE').addEventListener('change', function(){
        mode_update(document.getElementById('MODE').value);
    })

    document.getElementById('ENDIAN').addEventListener('change', function(){
        endian_update(document.getElementById('ENDIAN').value);
    })

    document.getElementById('OFFSET').addEventListener('change', function(){
        offset_update(document.getElementById('OFFSET').value);
    })

    asm_editor.session.on('change', function(delta) {
        let asm_code = asm_editor.getValue();
        socket.emit('assemble', {'code':asm_code})
    });
    //editor2.session.on('change', function(delta) {
        //if(lock){
            //return;
        //}
        //lock = true;
        //try{
            //let editorText = editor2.getValue();
            //let disasmText = handleDisasm(globalConfig,editorText);
            //editor.setValue(putInstructions(disasmText));
        //}catch(e){
            //console.log(e);
            //restoreDefault();
        //}
        //lock = false;
    //});
    
    socket.emit('get_settings');
}

function update_assembled_code(code)
{
    output_code = "";

    code.forEach(function(code_line){
        hexed_line = code_line.map(function(inp){return ("0"+inp.toString(16)).substr(-2).toUpperCase()}).join(' ')
        output_code += hexed_line + "\n"
    })

    machine_editor.setValue(output_code, 1)
}

function clear_option_element(element)
{
    while (document.getElementById(element).length != 0) document.getElementById(element).remove(0);
}

function offset_update(OFFSET)
{
    global_settings['OFFSET'] = OFFSET;

    socket.emit('update_settings', global_settings)
}

function endian_update(ENDIAN)
{
    global_settings['ENDIAN'] = ENDIAN;

    socket.emit('update_settings', global_settings)
}

function mode_update(MODE)
{
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
    else 
    {
        document.getElementById('ENDIAN').value = global_settings['ENDIAN']
        socket.emit('update_settings', global_settings)
    }

}

function arch_update(ARCH)
{
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
    else 
    {
        document.getElementById('MODE').value = global_settings['MODE']
        socket.emit('update_settings', global_settings)
    }


}


function handle_set_settings(settings)
{
    //Just change the ARCH, it will start a chain of event handlers...
    global_settings = settings;

    document.getElementById('ARCH').value = settings['ARCH']
    arch_update(settings['ARCH']);

    document.getElementById('MODE').value = settings['MODE']
    mode_update(settings['MODE']);
    
    document.getElementById('ENDIAN').value = settings['ENDIAN']
    endian_update(settings['ENDIAN']);

    document.getElementById('OFFSET').value = settings['OFFSET']
    offset_update(settings['OFFSET']);
}

