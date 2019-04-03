function toHex(buffer){
    if(buffer.constructor.name==='String'){
        buffer=buffer.split(" ");
    }
    temp = [];
    buffer.map(v=>{
        temp1 = (v).toString(16).toUpperCase();
        console.log(temp1);
        if(temp1.length===1){
            temp1="0"+temp1;
        }
        temp.push(temp1);
    })
    return temp;

}
function bufferToInt(buffer){
    if(buffer.constructor.name==="String"){
        buffer = filter2(buffer);
    }
    let temp =[];
    buffer.forEach(v=>{
        temp.push(parseInt(v,16));
    });
    return temp;
}

