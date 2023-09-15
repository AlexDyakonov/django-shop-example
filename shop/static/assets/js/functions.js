// Input number
const plus = document.querySelector(".plus"),
    minus = document.querySelector(".minus"),
    num = document.querySelector(".num");

let min = 1;
let a = min;

plus.addEventListener("click", ()=>{
    a++;
    num.innerText = a;
})

minus.addEventListener("click", ()=>{
    if ((--a) <= 1){
        a = 1;
    } else{
        a--;
    }

    num.innerText = a;
    console.log(a)
})

// Add to cart functionality

$(".to-cart-btn").on("click", function(event){
    event.preventDefault();

    if (is_authenticated) {
        var numText = document.querySelector('.num').textContent;
        var csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    
        let product_id = $(".product-id").val();
        let product_country = $("#soflow").val();
        let quantity = parseInt(numText);
        let product_price = $(".product-price").val();
        let this_val = $(this)
        
    
        console.log("Id:", product_id)
        console.log("Country ID:", product_country)
        console.log("Item qty:", quantity)
        console.log("Price:", product_price)
        console.log("CSRF Token:", "{{ csrf_token }}");
    
        $.ajaxSetup({
            headers: { "X-CSRFToken": "{{ csrf_token }}" }
        });
        $.ajax({
            type: 'POST',
            url: '/add-to-cart',
            data:{
                'id': product_id,
                'country': product_country,
                'qty': quantity,
                'price': product_price,
            },
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token); // csrf_token - значение токена
                console.log("Adding product to cart...")
            },
            success: function(){
                this_val.html("Добавлено")
                console.log("Added product to cart.")
            },
        })
    } else {
        alert("Пользователь не авторизован. Войдите в систему, чтобы добавить товар в корзину.");
    }
   
})