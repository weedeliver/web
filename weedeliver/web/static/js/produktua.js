function increment() {
  let number = parseInt(document.getElementById('kantitatea').value, 10);
  let numberInput = document.getElementById('kantitatea');
  let numberVisible = document.getElementById('kantitateav');
  number++;
  if(number > 99) number = 99; // to enforce the max value
  numberInput.value = number;
  numberVisible.innerText = number.toString();
}

function decrement() {
  let number = parseInt(document.getElementById('kantitatea').value, 10);
  let numberInput = document.getElementById('kantitatea');
  let numberVisible = document.getElementById('kantitateav');
  number--;
  if(number < 1) number = 1; // to enforce the max value
  numberInput.value = number;
  numberVisible.innerText = number.toString();
}
