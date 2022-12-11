init()


function init(){
    let pages = document.getElementsByName("page");
    pages[0].style.display = 'block'; 
    localStorage.setItem("cur_page", 0);
}

function nextPage(){
    let cur_page = Number(localStorage.getItem("cur_page"));
    let pages = document.getElementsByName("page");
    if (cur_page != pages.length - 1){
        
        pages[cur_page].style.display = 'none';
        cur_page += 1;
        pages[cur_page].style.display = 'block';

        localStorage.setItem("cur_page", cur_page);
    }

}

function prevPage(){
    let cur_page = Number(localStorage.getItem("cur_page"));
    let pages = document.getElementsByName("page");
    if (cur_page != 0){
        
        pages[cur_page].style.display = 'none';
        cur_page -= 1;
        pages[cur_page].style.display = 'block';

        localStorage.setItem("cur_page", cur_page);
    }

}