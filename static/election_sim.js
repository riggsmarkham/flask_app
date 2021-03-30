var selection = [];
button_list = document.getElementsByTagName('button');
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
    }
    console.log(selection);
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
            reveal_appr_form();
        }
    } else {
        if (selection[3] == "file"){
            reveal_file_submission();
        } else {
            reveal_pair_form();
        }
    }
}