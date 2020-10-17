let updateBtns = document.getElementsByClassName('update-cart') 

for (i = 0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log(productId, action)
        updateItem(productId, action)
        
    })
}

function updateItem(productId, action){

    let url = '/add-to-chart/'
    fetch(url, {
        method: 'POST', 
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            'Content-Type': 'application/json',
        },
        body:JSON.stringify({'productId': productId, 'action':action})
    })
    .then((response)=>{
        return response.json();
    })
    .then((data)=>{
      location.reload();
    });
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}