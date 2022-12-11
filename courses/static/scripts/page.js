function addTextArea(){
    let num = document.querySelectorAll('textarea').length
    let root = document.getElementById("formRoot");
    let label = document.createElement("label");
    label.setAttribute("for", "text" + (num));
    label.textContent = "Текст " + (num + 1);
    label.classList.add("form-label");
    root.appendChild(label);
    let area = document.createElement("textarea");
    area.name = "text" + num;
    area.id = "text" + num;
    area.rows = 10;
    area.cols = 30;
    area.classList.add("form-control");
    area.classList.add("mb-4");

    document.getElementById("order").value = document.getElementById("order").value + ' ' + "text" + num;

    root.appendChild(area);
}

function addImage(){
    let num = document.querySelectorAll('input[type=file]').length;
    let root = document.getElementById("formRoot");
    let label = document.createElement("label");
    label.setAttribute("for", "img" + num);
    label.textContent = "Изображение " + (num + 1);
    label.classList.add("form-label");
    root.appendChild(label);
    let img_inp = document.createElement("input");
    img_inp.type = "file"
    img_inp.name = "img" + num;
    img_inp.id = "img" + num;
    img_inp.rows = 10;
    img_inp.cols = 30;
    img_inp.classList.add("form-control");
    img_inp.classList.add("mb-4");

    document.getElementById("order").value = document.getElementById("order").value + ' ' + "img" + num;

    root.appendChild(img_inp);
}

function setFin(){
    document.getElementById('is_fin').value = true;
}