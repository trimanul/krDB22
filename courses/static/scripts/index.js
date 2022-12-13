function changeDiff(id){
    console.log(id);
    diff_h = document.getElementById(id);
    if (diff_h.innerText == "Легкий"){
      diff_h.classList.add('text-success');
    }

    if (diff_h.innerText == "Средний"){
      diff_h.classList.add('text-primary');
    }

    if (diff_h.innerText == "Сложный"){
      diff_h.classList.add('text-danger');
    }

  }