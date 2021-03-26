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
    //document.getElementById('displaything').innerHTML = selection;
}

function submit(){
    if(selection[2] == "fptp"){
        if (selection[3] == "file"){
            reveal_file_submission()
        } else {

        }
    } else if (selection[2] == "pref") {
        if (selection[3] == "file"){
            reveal_file_submission()
        } else {

        }
    } else if (selection[2] == "appr") {
        if (selection[3] == "file"){
            reveal_file_submission()
        } else {

        }
    } else {
        if (selection[3] == "file"){
            reveal_file_submission()
        } else {

        }
    }
}

function reveal_file_submission(){
    document.getElementById('sub_form').style.visibility = 'visible'
}