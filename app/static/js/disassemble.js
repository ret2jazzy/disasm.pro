function send_machine_update(){
    let machine_code_parsed;
    //Remove all non hex things
    let machine_code = machine_editor.getValue();
    if(document.getElementById('VIEW').value === "1")
        machine_code_parsed = parse_prettified(machine_code)
    else machine_code_parsed = parse_raw(machine_code)

    //global_settings.machine_code_bytes = machine_code_parsed;

    //socket.emit('disassemble', {'code':machine_code_parsed})

}

function update_disassembled_code(code){
    mutex_lock = true;
    asm_editor.setValue(code,1);
    mutex_lock = false;
}

function parse_raw(code){
    let raw_parsed = JSON.parse('"' + code.replace(/\\x/g, "\\u00") + '"'); // A super shitty hack to parse raw strings
    let machines_parsed = []
    //conver to array of ints
    raw_parsed.forEach(c => machine_parsed.push(c.charCodeAt(0)))

    return [].push(machine_parsed) //Because of the structure of machine_code_bytes
}

function parse_prettified(code){
    let code_splitted = code.split("\n")
    let machine_parsed = []
    
    code_splitted.forEach(function(code_line) {
        code_line = code_line.replace(/\s/g, "");
        if(code_line.length&1 != 0)throw "Not valid hex"
        //convert to int array from hex
        let parsed_hex = []
        for(let i = 0; i < code_line.length; i+=2){
           parsed_hex.push(parseInt(code.substr(i, i+2), 16))
        }
        machine_parsed.push(parsed_hex);
    })

    return machine_parsed
}
