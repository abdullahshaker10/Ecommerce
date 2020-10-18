let updateBtns = document.getElementsByClassName('update-cart') 

for (i = 0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        let productId = this.dataset.product
        let action = this.dataset.action
        let orderId = this.dataset.order
        let itemId = this.dataset.item
        console.log(itemId)
        
        update(productId, action, orderId, itemId)
        
    })
}

function update(productId, action, orderId, itemId){

    if (itemId){
        updateItems(productId, action, orderId, itemId)

    }
    else{
        updateChart(productId, action, orderId)
    }
    
}


function updateItems(productId, action, orderId, itemId)
{
    let url = '/api/items/'+itemId
        fetch(url, {
            method: 'PATCH', 
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                'Content-Type': 'application/json',
            },
            body:JSON.stringify({'productId': productId, 'action':action, 'order' : orderId, 'item': itemId})
        })
        .then((response)=>{
            return response.json();
        })
        .then((data)=>{
          console.log('data is: ', data)
          document.getElementById(itemId).innerHTML = data['quantity']


        });
}

function updateChart(productId, action, orderId){
    let url = '/api/orders/'+orderId
        fetch(url, {
            method: 'PATCH', 
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                'Content-Type': 'application/json',
            },
            body:JSON.stringify({'productId': productId, 'action':action, 'order' : orderId})
        })
        .then((response)=>{
            return response.json();
        })
        .then((data)=>{
          console.log('data is: ', data)
          document.getElementById('cart-total').innerHTML = data['cart_total']
           
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