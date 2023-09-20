const paymentComissionElement = document.getElementById("comission");
const orderTotalElement = document.getElementById("order-total");
const selectElement = document.querySelector("#soflow");
const orderTotalNoComission =  parseFloat(orderTotalElement.textContent)

selectElement.addEventListener("change", function () {
    const selectedOption = selectElement.options[selectElement.selectedIndex];
    const comissionValue = selectedOption.value;

    let comission = parseFloat(selectedOption.value);
    
    let order_total = orderTotalNoComission + comission;

    orderTotalElement.textContent = order_total

    paymentComissionElement.textContent = comissionValue;
});

document.addEventListener("DOMContentLoaded", function() {
    const selectedOption = selectElement.options[selectElement.selectedIndex];
    const comissionValue = selectedOption.value;
    paymentComissionElement.textContent = comissionValue;
});

var redirectButton = document.getElementById('to-cart-button');
  
redirectButton.addEventListener('click', function() {
  window.location.href = '{% url 'core:cart' %}';
});

var toPaymentButton = document.getElementById('to-payment-button');


// to payment
toPaymentButton.on("click", function(event){
    event.preventDefault();

    if (is_authenticated) {
        var csrf_token = $("input[name='csrfmiddlewaretoken']").val();

        let total_order_price = $("#order-total").val();
        
        console.log("Price:", total_order_price)
        console.log("CSRF Token:", csrf_token);
    }else {
        alert("Пользователь не авторизован. Войдите в систему, чтобы перейти к оплате.");
    }

    $.ajaxSetup({
        headers: { "X-CSRFToken": "{{ csrf_token }}" }
    });
    $.ajax({
        type: "POST",
        url: "/checkout",
        data: {
            'total_order_price': total_order_price
        },
        dataType: 'json',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
            console.log("Creating order...")
        },
        success: function(response) {
            console.log("Success:", response);
        },
        error: function(xhr, errmsg, err) {
            console.log("Error:", errmsg);
        }
    });
})