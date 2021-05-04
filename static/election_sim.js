//setup
const UPLOAD_RESULT = 'results';
const UPLOAD_FILEEXT = '.txt';
const IMGFILEFORMAT = '.png'
const UPLOAD_IMAGES = 'img';
const UPLOAD_FOLDER = 'static/election_sim_images'

var selection = [];
var filename_root = "";

$.ajaxSetup({processData: false, contentType: false});

const total_button_list = document.getElementsByTagName('button');
var button_list = Array(0);
var bot_button_list = Array(0);
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

document.getElementById('top_div').style.display = 'block';

//processes click on one of the buttons in the selector part
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
        const num = parseInt(clicked_el.id.slice(0,1));
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

//processes a click on the button to go into the form
function submit(el){
    el.classList.add('clicked');
    for(but of button_list){
        but.style.display = 'none';
    }
    document.getElementById('top_div').style.display = 'none';
    if (selection[3] == "file"){
        document.getElementById('file_form').style.display = 'block';
    } else {
        document.getElementById('cand_table').style.display = 'none';
        document.getElementById('poll_table').style.display = 'none';
        document.getElementById('text_form').style.display = 'block';
    }
}

//creates the table to input the candidate names
function populate_cand_table(){
    const num = parseInt(document.getElementById("cand_num").value);
    const newTable = document.createElement("table");
    newTable.id="cands";
    var r, c;
    for (i = 0; i < num; i++){
        r = newTable.insertRow();
        c = r.insertCell();
        c.innerHTML = "<input type = 'text'></input>";
    }
    const parent = document.getElementById("cand_table");
    const child = document.getElementById("pref_q");
    parent.insertBefore(newTable, child);
    document.getElementById("cand_setup").style.display='none';
    if(selection[2] != "pref"){
        child.style.display = 'none';
    }
    parent.style.display='block';
}

//creates the page to input the polling data
function populate_poll_table(){
    const childArray = Array.from(document.getElementById("cands").childNodes[0].childNodes);
    var candNames = Array(0);
    for(el of childArray){
        candNames.push(el.childNodes[0].childNodes[0].value);
    }
    var table;
    if(selection[2] == "fptp"){
        table = create_poll_table_element(candNames, "Candidate Name", "Poll Result");
    } else if (selection[2] == "pref"){
        const val = parseInt(document.getElementById("pref_len").value);
        const permutedArr = getPermutations(candNames, val);
        var newArray = [];
        for (i = 0; i < permutedArr.length; i++){
            newArray.push(permutedArr[i].join(">"));
        }
        table = create_poll_table_element(newArray, "Preference List", "Poll Result");
    } else if (selection[2] == "appr"){
        table = create_poll_table_element(candNames, "Candidate Name", "Approval Rating");
    } else if (selection[2] == "pair"){
        const combinationArr = getCombinations(candNames, 2);
        var newArray = [];
        for (i = 0; i < combinationArr.length; i++){
            newArray.push(combinationArr[i].join(">"));
        }
        table = create_poll_table_element(newArray, "Pair of Candidates", "Poll Result");
    }
    const parent = document.getElementById("poll_table");
    const child = document.getElementById("ss_q");
    parent.insertBefore(table, child);
    document.getElementById("cand_table").style.display='none';
    document.getElementById("poll_table").style.display='block';
}

//creates the poll table itself
function create_poll_table_element(array, col_1, col_2){
    const newTable = document.createElement("table");
    newTable.id="polls";
    var r = newTable.insertRow();
    var c = r.insertCell();
    c.innerHTML = col_1;
    c = r.insertCell();
    c.innerHTML = col_2;
    for (i = 0; i < array.length; i++){
        r = newTable.insertRow();
        c = r.insertCell();
        c.innerHTML = array[i];
        c = r.insertCell();
        c.innerHTML = "<input type = 'number'></input>";
    }
    return newTable;
}

//process text input from the user and send it to the server
function process_input(){
    const childNameArray = Array.from(document.getElementById("cands").childNodes[0].childNodes);
    var candNames = Array(0);
    for(el of childNameArray){
        candNames.push(el.childNodes[0].childNodes[0].value);
    }
    const childPollArray = Array.from(document.getElementById("polls").childNodes[0].childNodes);
    var pollNums = Array(0);
    for(el of childPollArray){
        pollNums.push(el.childNodes[1].childNodes[0].value);
    }
    pollNums.shift();
    var sample_size = document.getElementById("ss_num").value;
    var candString = candNames.join();
    var pollString = pollNums.join();
    var text = '1\n'+candString+'\n'+pollString+'\n'+sample_size+'\n';
    if(selection[2] == "fptp"){
        text += '1';
    } else if(selection[2] == "pref"){
        text += document.getElementById('pref_len').value;
    } else if(selection[2] == "appr"){
        text += 'a';
    } else if(selection[2] == "pair"){
        text += 'p';
    }
    var formData = new FormData();
    formData.append('text', text);
    $.post('/election_sim/text_submit', formData, function(res){
        create_processed_block(res);
    });
}

//upload a file to the server
function upload_file(){
    var formData = new FormData();
    formData.append("file", document.getElementById('fileupload').files[0]);
    $.post('/election_sim/file_submit', formData, function(res){
        create_processed_block(res);
    });
}

//retrieve processed data from server and create block displaying
function create_processed_block(res){
    const obj = JSON.parse(res);
    filename_root = obj.filename_root
    var table;
    if(selection[2] == "fptp"){
        document.getElementById('pb_cand_list').innerHTML += obj.candString;
        document.getElementById('pb_ss').innerHTML += obj.sample_size;
        const candArray = obj.candString.split(", ");
        document.getElementById('pb_cand_num').innerHTML += candArray.length.toString();
        const numArray = obj.pollString.split(", ");
        table = create_poll_table_processed(candArray, numArray, "Candidate Name", "Poll Result");
    } else if (selection[2] == "pref"){
        document.getElementById('pb_cand_list').innerHTML += obj.candString;
        document.getElementById('pb_ss').innerHTML += obj.sample_size;
        const candArray = obj.candString.split(", ");
        document.getElementById('pb_cand_num').innerHTML += candArray.length.toString();
        const numArray = obj.pollString.split(", ");
        const val = parseInt(document.getElementById("pref_len").value);
        const permutedArr = getPermutations(candArray, val);
        console.log(permutedArr);
        var newArray = [];
        for (i = 0; i < permutedArr.length; i++){
            newArray.push(permutedArr[i].join(">"));
        }
        console.log(newArray);
        table = create_poll_table_processed(newArray, numArray, "Preference List", "Poll Result");
    } else if (selection[2] == "appr"){
        document.getElementById('pb_cand_list').innerHTML += obj.candString;
        document.getElementById('pb_ss').innerHTML += obj.sample_size;
        const candArray = obj.candString.split(", ");
        document.getElementById('pb_cand_num').innerHTML += candArray.length.toString();
        const numArray = obj.pollString.split(", ");
        table = create_poll_table_processed(candArray, numArray, "Candidate Name", "Approval Result");
    } else if (selection[2] == "pair"){
        document.getElementById('pb_cand_list').innerHTML += obj.candString;
        document.getElementById('pb_ss').innerHTML += obj.sample_size;
        const candArray = obj.candString.split(", ");
        document.getElementById('pb_cand_num').innerHTML += candArray.length.toString();
        const numArray = obj.pollString.split(", ");
        const combinationArr = getCombinations(candArray, 2);
        var newArray = [];
        for (i = 0; i < combinationArr.length; i++){
            newArray.push(combinationArr[i].join(">"));
        }
        table = create_poll_table_processed(newArray, numArray, "Candidate Pair", "Poll Result");
    }
    const parent = document.getElementById("process_box");
    const child = document.getElementById("pb_ss");
    parent.insertBefore(table, child);
    document.getElementById("poll_table").style.display='none';
    document.getElementById("file_form").style.display='none';
    document.getElementById("0-download-file-link").href = '/election_sim/download_file/' + filename_root + UPLOAD_FILEEXT;
    parent.style.display='block';
}

//creates the processed poll table
function create_poll_table_processed(array_1, array_2, col_1, col_2){
    const newTable = document.createElement("table");
    newTable.id="processed_polls";
    var r = newTable.insertRow();
    var c = r.insertCell();
    c.innerHTML = col_1;
    c = r.insertCell();
    c.innerHTML = col_2;
    for (i = 0; i < array_1.length; i++){
        r = newTable.insertRow();
        c = r.insertCell();
        c.innerHTML = array_1[i];
        c = r.insertCell();
        c.innerHTML = array_2[i];
    }
    return newTable;
}

//run the current file through the the simulator
function run(){
    $.getJSON('/election_sim/run_file/' + filename_root + UPLOAD_FILEEXT, function(res) {
        console.log(res.textResult);
        properString = res.textResult.replaceAll('\n','<br>');
        create_image_block(res.imgFolderName, parseInt(res.numFiles));
        document.getElementById("result_p").innerHTML = properString;
        document.getElementById("process_box").style.display = 'none';
        document.getElementById("0-download-results-link").href = '/election_sim/download_file/' + filename_root + UPLOAD_RESULT + UPLOAD_FILEEXT;
        document.getElementById("result_box").style.display = 'block';
    });
}

//delete file and restart the form
function delete_file(){
    $.ajax({
        url: '/election_sim/delete_file/' + filename_root + UPLOAD_FILEEXT,
        method: 'DELETE',
        success: function() {
            $.ajax({
                url: '/election_sim/delete_file/' + filename_root + UPLOAD_IMAGES,
                method: 'DELETE',
                success: function() {
                    document.getElementById("0-run-file").disabled = true;
                    document.getElementById("0-download-file").disabled = true;
                    document.getElementById("0-delete-file").disabled = true;
                }
            });
        }
    });
}

//create place for image files to go
function create_image_block(imgfoldername, num){
    for (i = 0; i < num; i++){
        var img;
        num_str = i.toString();
        img = document.createElement('img');
        img.src = '/' + UPLOAD_FOLDER + '/' + imgfoldername + '/' + num_str + IMGFILEFORMAT;
        img.alt = 'Simulation ' + num_str;
        img.id = UPLOAD_IMAGES + num_str;
        const parent = document.getElementById('result_box');
        const child = document.getElementById('0-download-results-link');
        parent.insertBefore(img, child);
    }
}

//a function that I found that should find all combinations an array
//https://stackoverflow.com/questions/45813439/itertools-combinations-in-javascript
function getCombinations(array, size) {
    function p(t, i) {
        if (t.length === size) {
            result.push(t);
            return;
        }
        if (i + 1 > array.length) {
            return;
        }
        p(t.concat(array[i]), i + 1);
        p(t, i + 1);
    }
    var result = [];
    p([], 0);
    return result;
}

//a function that I found that should find all permutations of an array
//https://gist.github.com/justinfay/f30d53f8b85a274aee57
function getPermutations(array, r) {
    // Algorythm copied from Python `itertools.permutations`.
    var n = array.length;
    if (r === undefined) {
        r = n;
    }
    if (r > n) {
        return;
    }
    var indices = [];
    for (var i = 0; i < n; i++) {
        indices.push(i);
    }
    var cycles = [];
    for (var i = n; i > n - r; i--) {
        cycles.push(i);
    }
    var results = [];
    var res = [];
    for (var k = 0; k < r; k++) {
        res.push(array[indices[k]]);
    }
    results.push(res);
    var broken = false;
    while (n > 0) {
        for (var i = r - 1; i >= 0; i--) {
            cycles[i]--;
            if (cycles[i] === 0) {
                indices = indices.slice(0, i).concat(
                    indices.slice(i + 1).concat(
                        indices.slice(i, i + 1)));
                cycles[i] = n - i;
                broken = false;
            } else {
                var j = cycles[i];
                var x = indices[i];
                indices[i] = indices[n - j];
                indices[n - j] = x;
                var res = [];
                for (var k = 0; k < r; k++) {
                    res.push(array[indices[k]]);
                }
                results.push(res);
                broken = true;
                break;
            }
        }
        if (broken === false) {
            break;
        }
    }
    return results;
}