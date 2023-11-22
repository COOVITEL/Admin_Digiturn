let button1 = document.querySelector('.bt1');
let button2 = document.querySelector('.bt2');
let login = document.querySelector('.login');
let register = document.querySelector('.register');

button1.addEventListener("click", function() {
    button1.classList.add("act")
    button2.classList.remove("act")
    login.classList.add("see")
    register.classList.remove("see")
})

button2.addEventListener("click", function() {
    button2.classList.add("act")
    button1.classList.remove("act")
    register.classList.add("see")
    login.classList.remove("see")
})


function formatNumber(input) {
    // Obtener el valor del campo de entrada
    let value = input.value;
    //let val = value.replace(",", "")
    let rev = reverseString(value)
    let setVal = rev.replace(/\D/g, '')
    let formatVal = setVal.replace(/(\d{3})/g, '\$1.')
    let newVla = reverseString(formatVal)
    if (newVla[0] == "."){
      newVla = newVla.slice(1)
    }
    console.log(newVla)
    input.value = newVla;
}

function reverseString(str) {
    return str.split('').reverse().join('')
}