function send_machine_update(){
    //Remove all non hex things
    let machine_code = machine_editor.getValue();

    //handle all parsing server side
    socket.emit('disassemble', {'code':machine_code, 'view' : document.getElementById('VIEW').value})

}

function update_disassembled_code(code){
    mutex_lock = true;
    asm_editor.setValue(code,1);
    mutex_lock = false;

}

