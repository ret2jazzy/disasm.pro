function send_asm_update(){
    let asm_code = asm_editor.getValue();
    socket.emit('assemble', {'code':asm_code})
}

function update_assembled_prettified(code){
    output_code = "";

    code.forEach(function(code_line){
        hexed_line = Array.from(new Uint8Array(code_line)).map(function(inp){return ("0"+inp.toString(16)).substr(-2).toUpperCase()}).join(' ')
        output_code += hexed_line + "\n"
    })

    mutex_lock = true
    machine_editor.setOption("wrap", false); //Don't wrap
    machine_editor.setValue(output_code, 1);
    //move cursor simultaneously
    let cur_line = asm_editor.selection.getCursor().row;
    machine_editor.selection.moveTo(cur_line, 0);

    mutex_lock = false;

}

function update_assembled_raw(code){
    let output_code = ""

    code.forEach(function(code_line){
        hexed_line_raw = Array.from(new Uint8Array(code_line)).map(function(inp){return "\\x"+ ("0"+inp.toString(16)).substr(-2).toUpperCase()}).join('')
        output_code += hexed_line_raw
    })
    mutex_lock = true
    machine_editor.setOption("wrap", true); //wrap lines for raw string
    machine_editor.setValue(output_code, 1);
    mutex_lock = false;

}

function update_assembled_code(code){
    global_settings.machine_code_bytes = JSON.stringify(code);// Update the code bytes in local storage for when we change modes

    if (global_settings['VIEW'] == '1')
        update_assembled_prettified(code)
    else update_assembled_raw(code);

    set_success_message("Code Assembled")

}
