var selection = [];
total_button_list = document.getElementsByTagName('button');
button_list = Array(0);
for(el of total_button_list){
    if(el.id.slice(0,1) != "0"){
        button_list.push(el);
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
    button_list = document.getElementsByTagName('button');
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
        for(el of document.getElementsByTagName('form')){
            el.style.display = 'none';
        }
    }
    console.log(selection);
    //document.getElementById('displaything').innerHTML = selection;
}

function submit(el){
    document.getElementById('fptp_input').style.display = 'none';
    if(selection[2] == "fptp"){
        if (selection[3] == "file"){
            reveal(['file_form'],el)
        } else {
            reveal(['fptp_form'],el)
        }
    } else if (selection[2] == "pref") {
        if (selection[3] == "file"){
            reveal(['file_form'],el)
        } else {
            reveal(['pref_form'],el)
        }
    } else if (selection[2] == "appr") {
        if (selection[3] == "file"){
            reveal(['file_form'],el)
        } else {
            reveal(['appr_form'],el)
        }
    } else {
        if (selection[3] == "file"){
            reveal(['file_form'],el)
        } else {
            reveal(['pair_form'],el)
        }
    }
}

function populate_fptp_form(){
    var val = document.getElementById("fptp_num").value;
    addTable(val,"Candidate Name", "Percent Support", "fptp_input", "fptp_input_sub")
    document.getElementById("fptp_input").style.display='inline';
    document.getElementById("fptp_setup").style.display='none';
}

function populate_appr_form(){
    var val = document.getElementById("appr_num").value;
    addTable(val,"Candidate Name", "Percent Approval", "appr_input", "appr_input_sub")
    document.getElementById("appr_input").style.display='inline';
    document.getElementById("appr_setup").style.display='none';
}

function addTable(val, col_1, col_2, parent_id, child_id){
    const newTable = document.createElement("table");
    num = parseInt(val);
    var r = newTable.insertRow();
    var c = r.insertCell();
    c.innerHTML = col_1;
    c = r.insertCell();
    c.innerHTML = col_2;
    for (i = 1; i < num + 1; i++){
        r = newTable.insertRow();
        c = r.insertCell();
        c.innerHTML = "<input id=txt" + i.toString() + "-1 type = 'text'></input>";
        c = r.insertCell();
        c.innerHTML = "<input id=txt" + i.toString() + "-2 type = 'text'></input>";
    }
    var parent = document.getElementById(parent_id);
    var child = document.getElementById(child_id);
    parent.insertBefore(newTable, child);
}