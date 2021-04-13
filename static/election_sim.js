var selection = [];
total_button_list = document.getElementsByTagName('button');
button_list = Array(0);
bot_button_list = Array(0);
for(el of total_button_list){
    if(el.id.slice(0,1) != "0"){
        button_list.push(el);
    } else {
        bot_button_list.push(el);
    }
}

for(el of button_list){
    if(el.id.slice(0,1) == "1"){
        el.style.display = 'inline';
    } else {
        el.style.display = 'none';
    }
}

function reveal(el_list, clicked_el){
    if(!clicked_el.classList.contains('clicked')){
        clicked_el.classList.add('clicked');
        selection.push(clicked_el.id.slice(2));
        for(el of el_list){
            document.getElementById(el).style.display = 'inline';
        }
        for(el of button_list){
            if((el.id.slice(0,1) == clicked_el.id.slice(0,1)) & (el.id != clicked_el.id)){
                el.disabled = true;
            }
        }
    } else {
        clicked_el.classList.remove('clicked')
        num = parseInt(clicked_el.id.slice(0,1));
        selection = selection.slice(0,num - 1);
        for(el of button_list){
            if(el.id.slice(0,1) == clicked_el.id.slice(0,1)){
                el.disabled = false;
            }
        };
        for(el of button_list){
            if(parseInt(el.id.slice(0,1)) > num){
                el.classList.remove('clicked');
                el.disabled = false;
                el.style.display = 'none';
            }
        }
    }
    console.log(selection);
}

function submit(el){
    el.classList.add('clicked');
    for(but of button_list){
        but.style.display = 'none';
    }
    if (selection[3] == "file"){
        document.getElementById('file_form').style.display = 'block';
    } else {
        document.getElementById('cand_table').style.display = 'none';
        document.getElementById('poll_table').style.display = 'none';
        document.getElementById('text_form').style.display = 'block';
    }
}

function populate_cand_table(){
    var val = document.getElementById("cand_num").value;
    const newTable = document.createElement("table");
    newTable.id="cands";
    num = parseInt(val);
    for (i = 0; i < num; i++){
        var r = newTable.insertRow();
        var c = r.insertCell();
        c.innerHTML = "<input type = 'text'></input>";
    }
    const parent = document.getElementById("cand_table");
    const child = document.getElementById("pref_q");
    parent.insertBefore(newTable, child);
    document.getElementById("cand_setup").style.display='none';
    if(selection[2] != "pref"){
        child.style.display = 'none';
    }
    document.getElementById("cand_table").style.display='block';
}

function populate_poll_table(){
    const childArray = Array.from(document.getElementById("cands").childNodes[0].childNodes);
    console.log(childArray.length);
    console.log(childArray[0].childNodes[0].nodeName);
    var candNames = Array(0);
    for(el of childArray){
        candNames.push(el.childNodes[0].childNodes[0].value);
    }
    var table;
    if(selection[2] == "fptp"){
        table = create_poll_table_element(candNames, "Candidate Name", "Poll Result");
    } else if (selection[2] == "pref"){
        //var val = document.getElementById("pref_len").value;

    } else if (selection[2] == "appr"){
        table = create_poll_table_element(candNames, "Candidate Name", "Approval Rating");
    } else if (selection[2] == "pair"){

    }
    const parent = document.getElementById("poll_table");
    const child = document.getElementById("ss_q");
    parent.insertBefore(table, child);
    document.getElementById("cand_table").style.display='none';
    document.getElementById("poll_table").style.display='block';
}

function create_poll_table_element(array, col_1, col_2){
    const newTable = document.createElement("table");
    newTable.id="polls";
    var r = newTable.insertRow();
    var c = r.insertCell();
    c.innerHTML = col_1;
    var c = r.insertCell();
    c.innerHTML = col_2;
    for (i = 0; i < array.length; i++){
        var r = newTable.insertRow();
        var c = r.insertCell();
        c.innerHTML = array[i];
        var c = r.insertCell();
        c.innerHTML = "<input type = 'number'></input>";
    }
    return newTable;
}