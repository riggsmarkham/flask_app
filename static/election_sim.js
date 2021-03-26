var selection = [];
function toggle_display(class_name, row_name, clicked_el){
    if(!clicked_el.classList.contains('clicked')){
        clicked_el.classList.add('clicked')
        selection.push(class_name);
        class_items = document.getElementsByClassName(class_name);
        for(el of class_items){
            el.style.visibility = 'visible'
        };
        row_items = document.getElementsByClassName(row_name);
        for(el of row_items){
            el.disabled = true;
        };
        clicked_el.disabled = false;
    }else{
        clicked_el.classList.remove('clicked')
        selection.pop();
        row_items = document.getElementsByClassName(row_name);
        for(el of row_items){
            el.disabled = false;
        };
        if(document.getElementsByClassName(class_name)[0]){
            next_row_items = document.getElementsByClassName(document.getElementsByClassName(class_name)[0].classList[0])
            for(el of next_row_items){
                el.style.visibility = 'hidden'
            };
        }
    }
    console.log(selection)
    //document.getElementById('displaything').innerHTML = selection;
}

function submit(){
    if(selection[2] == "fptp"){
        if (selection[3] == "file"){
            reveal_file_submission();
        } else {
            reveal_fptp_form();
        }
    } else if (selection[2] == "pref") {
        if (selection[3] == "file"){
            reveal_file_submission();
        } else {
            reveal_pref_form();
        }
    } else if (selection[2] == "appr") {
        if (selection[3] == "file"){
            reveal_file_submission();
        } else {
            reveal_appr_form()
        }
    } else {
        if (selection[3] == "file"){
            reveal_file_submission()
        } else {
            reveal_pair_form()
        }
    }
}

function reveal_file_submission(){
    document.getElementById('sub_form').style.visibility = 'visible'
}

function reveal_fptp_form(){
    document.getElementById('fptp_form').style.visibility = 'visible'
}

function reveal_pref_form(){
    document.getElementById('pref_form').style.visibility = 'visible'
}

function reveal_appr_form(){
    document.getElementById('appr_form').style.visibility = 'visible'
}

function reveal_pair_form(){
    document.getElementById('pair_form').style.visibility = 'visible'
}