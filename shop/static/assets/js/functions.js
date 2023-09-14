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

    var numText = document.querySelector('.num').textContent;

    let product_title = $(".product-title").val();
    let product_id = $(".product-id").val();
    let product_country = $("#soflow").val();
    let quantity = parseInt(numText);
    let product_price = $(".product-price").val();
    let this_val = $(this)
    

    console.log("Title:", product_title)
    console.log("Id:", product_id)
    console.log("Country ID:", product_country)
    console.log("Item qty:", quantity)
    console.log("Price:", product_price)

    $.ajax({
        url: '/add-to-cart',
        data:{
            'id': product_id,
            'title': product_title,
            'country': product_country,
            'qty': quantity,
            'price': product_price,
        },
        dataType: 'json',
        beforeSend: function(){
            console.log("Adding product to cart...")
        },
        success: function(){
            this_val.html("Добавлено")
            console.log("Added product to cart.")
        }
    })
})