// Input number
const plusButtons = document.querySelectorAll(".plus");
const minusButtons = document.querySelectorAll(".minus");
const numElements = document.querySelectorAll(".num");

plusButtons.forEach((plusButton, index) => {
    var curr_pathname = '/cart/';

    if (currentLanguage=="ru"){
        curr_pathname='/ru/cart/'
    } else {
        curr_pathname='/en/cart/'
    }

    var csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    const minusButton = minusButtons[index];
    const numElement = numElements[index];
    const cart_item_id = numElement.id; 
    let quantity = parseInt(numElement.innerText);

    plusButton.addEventListener("click", () => {
        quantity++;
        numElement.innerText = quantity;
        if (window.location.pathname === curr_pathname){
            console.log("cart")
            updateCartItem(cart_item_id, quantity); 
        }
    });

    minusButton.addEventListener("click", () => {
        if (quantity > 1) {
            quantity--;
            numElement.innerText = quantity;
            if (window.location.pathname === curr_pathname){
                updateCartItem(cart_item_id, quantity); 
            }
        }
    });

    function updateCartItem(cart_item_id, quantity) {
        $.ajax({
            type: 'POST',
            url: '/update-cart-item', 
            data: {
                'cart_item_id': cart_item_id,
                'quantity': quantity,
                'csrfmiddlewaretoken': csrf_token 
            },
            dataType: 'json',
            success: function (response) {
                if (response.success) {
                    $('#total-item-' + cart_item_id).text(response.item_cart_total_price);
                    $('#pretotal-price').text(response.cart_total_price);
                    $('#total-price').text(response.cart_total_price);
                    console.log("Product updated in cart.");
                } else {
                    console.log("Error while updating product in cart.");
                }
            },
            error: function (xhr, textStatus, errorThrown) {
                console.log("Error while updating product in cart.");
            }
        });
    }
});

// Add to cart functionality

$(".to-cart-btn").on("click", function(event){
    event.preventDefault();
    if (currentLanguage == 'ru'){
        var added_btn = "Добавлено"
        var login_before = "Пользователь не авторизован. Войдите в систему, чтобы добавить товар в корзину."
    } else {
        var added_btn = "Added"
        var login_before = "The user is not logged in. Log in to add an item to the cart."
    }

    if (is_authenticated) {
        var numText = document.querySelector('.num').textContent;

        var csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    
        let product_id = $(".product-id").val();
        let product_country = $("#soflow").val();
        let quantity = parseInt(numText);
        
        quantity = quantity == 0 ? 1 : quantity;

        let product_price = $(".product-price").val();
        product_price = product_price.replace(/,/g, '.');

        let this_val = $(this)
        
    
        console.log("Id:", product_id)
        console.log("Country ID:", product_country)
        console.log("Item qty:", quantity)
        console.log("Price:", product_price)
    
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
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
                console.log("Adding product to cart...")
            },
            success: function(){
                this_val.html(added_btn);
                console.log("Added product to cart.")
            },
        })
    } else {
        alert(login_before);
    }
   
})

// remove from cart 
$(".remove_from_cart").on("click", function(event){
    event.preventDefault();

    if (is_authenticated) {
        var csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    
        var cart_item_id = $(this).data("cart-item-id");
        console.log(cart_item_id)
    
        console.log("Id:", cart_item_id)
        console.log("CSRF Token:", "{{ csrf_token }}");
    
        $.ajaxSetup({
            headers: { "X-CSRFToken": "{{ csrf_token }}" }
        });
        $.ajax({
            type: 'POST',
            url: '/remove-from-cart',
            data:{
                'id': cart_item_id,
            },
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
                console.log("Removing product from cart...")
            },
            success: function(response){
                if ('cart_is_empty' in response && response.cart_is_empty === true) {
                    console.log("reloaded")
                } else if ('cart_total_price' in response) {
                    console.log(cart_item_id)
                    $("#cart-item-" + cart_item_id).remove();
                    console.log("Removed product from cart. Id = " + cart_item_id )
                    $('#pretotal-price').text(response.cart_total_price);
                    $('#total-price').text(response.cart_total_price);
                    console.log("Product removed from cart.");
                    location.reload();
                } else {
                    console.log("Error while removing product from cart.");
                }
            },
        })
    } else {
        alert("Пользователь не авторизован. Войдите в систему, чтобы добавить товар в корзину.");
    }
})