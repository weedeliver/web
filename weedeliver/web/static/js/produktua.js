function increment() {
  let numberInput = document.getElementById('kantitatea');
  numberInput.value = parseInt(numberInput.value, 10) + 1;
  if(numberInput.value > 100) numberInput.value = 100; // to enforce the max value
}

function decrement() {
  let numberInput = document.getElementById('kantitatea');
  let currentValue = parseInt(numberInput.value, 10);
  if (currentValue > 1) { // changed from 0 to 1 to respect the min value
    numberInput.value = currentValue - 1;
  }
}
