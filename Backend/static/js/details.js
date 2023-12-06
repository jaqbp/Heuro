document.getElementById("submit-btn").addEventListener("click", function() {
  var values1 = document.getElementById("dziedzina").value;
  var values2 = document.getElementById("wymiar").value;
  var values3 = document.getElementById("iteracje").value;
  var values4 = document.getElementById("populacja").value;

  // Wyślij dane na backend
  fetch('/details', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ values1: values1,
        values2: values2,
        values3: values3,
        values4: values4 })
  })
  .then(response => response.text())
  .then(data => {
      console.log(data); // Odpowiedź z serwera
  })
  .catch(error => {
      console.error('Błąd:', error);
  });
});
