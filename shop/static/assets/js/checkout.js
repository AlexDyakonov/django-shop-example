const paymentComissionElement = document.getElementById("comission");
const orderTotalElement = document.getElementById("order-total");
const selectElement = document.querySelector("#soflow");
const orderTotalNoComission =  parseFloat(orderTotalElement.textContent)

selectElement.addEventListener("change", function () {
    const selectedOption = selectElement.options[selectElement.selectedIndex];
    const comissionValue = selectedOption.value;

    let comission = parseFloat(selectedOption.value);
    
    // let order_total = orderTotalNoComission + comission;

    orderTotalElement.textContent = order_total

    paymentComissionElement.textContent = comissionValue;
});

document.addEventListener("DOMContentLoaded", function() {
    const selectedOption = selectElement.options[selectElement.selectedIndex];
    const comissionValue = selectedOption.value;
    paymentComissionElement.textContent = comissionValue;
});

// to payment
