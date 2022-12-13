init()


function init(){
    let cur_page = Number(document.getElementById("cur_page").value.split(' ')[0]) - 1;
    let pages = document.getElementsByName("page");
    pages[cur_page].style.display = 'block'; 
    localStorage.setItem("cur_page", cur_page);
}

function nextPage(){
    let course_id = document.getElementById("cur_page").value.split(' ')[1];
    let cur_page = Number(localStorage.getItem("cur_page"));
    let cur_page_id = document.getElementById("cur_page").value.split(' ')[2];


    let pages = document.getElementsByName("page");
    if (cur_page != pages.length - 1){
        
        pages[cur_page].style.display = 'none';
        cur_page += 1;
        pages[cur_page].style.display = 'block';
        let csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value
        let xhttp = new XMLHttpRequest()
        xhttp.open("POST", "/api/change_cur", true);
        xhttp.setRequestHeader("X-CSRFToken", csrf);
        xhttp.send(JSON.stringify({"cur_page":(cur_page + 1), "course_id":course_id, "cur_page_id":cur_page_id}));

        localStorage.setItem("cur_page", cur_page);
    }

}

function prevPage(){
    let course_id = document.getElementById("cur_page").value.split(' ')[1];
    let cur_page = Number(localStorage.getItem("cur_page"));
    let cur_page_id = document.getElementById("cur_page").value.split(' ')[2];


    let pages = document.getElementsByName("page");
    if (cur_page >= 0){
        
        pages[cur_page].style.display = 'none';
        cur_page -= 1;
        pages[cur_page].style.display = 'block';
        let csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value
        let xhttp = new XMLHttpRequest()
        xhttp.open("POST", "/api/change_cur", true);
        xhttp.setRequestHeader("X-CSRFToken", csrf);
        xhttp.send(JSON.stringify({"cur_page":(cur_page + 1), "course_id":course_id, "cur_page_id":cur_page_id}));

        localStorage.setItem("cur_page", cur_page);
    }

}