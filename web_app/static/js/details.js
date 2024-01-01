function generateHTML(data) {
  const tableHeader = Object.keys(data.response)
    .map((k) => `<th>${k}</th>`)
    .join("");

  const tableRows = data.response[
    "Coefficient of variation of goal function value"
  ]
    .map((_, rowIndex) => {
      return `<tr>${Object.values(data.response)
        .map((columnData) => `<td>${columnData[rowIndex]}</td>`)
        .join("")}</tr>`;
    })
    .join("");

  const tableStyles = `
  <style>
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }

    th, td {
      border: 1px solid #dddddd;
      padding: 8px;
      text-align: left;
    }

    th {
      background-color: #f2f2f2;
    }
  </style>
`;

  return `
  <html>
    <head>
      <title>Your Generated HTML Page</title>
      ${tableStyles}
    </head>
    <body>
      <table>
        ${tableHeader}
        ${tableRows}
      </table>
    </body>
  </html>
  `;
}

const submitButton = document.getElementById("submit-btn");
const modal = document.getElementById("reportStateModal");
const stopBtn = document.getElementById("stopBtn");
const timerElement = document.getElementById("timer");
const modalText = document.getElementById("modalText");

let isRunning = true;
let isModalOpen = false;
let time = 0;

submitButton.addEventListener("click", async () => {
    modal.style.display = "block";
    isModalOpen = true;
    const domain = document.getElementById("dziedzina").value;
    const dimension = document.getElementById("wymiar").value;
    const numberOfIterations = document.getElementById("iteracje").value;
    const population = document.getElementById("populacja").value;

    const res = await fetch("http://127.0.0.1:5000/generate_text_report", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            domain,
            dimension,
            numberOfIterations,
            population,
        }),
    });

    if (!res.ok) {
        throw new Error("Error while setting details");
    }

    const data = await res.json();
    const html = generateHTML(data);
    const blob = new Blob([html], { type: "text/html" });
    const url = URL.createObjectURL(blob);
    window.location.href = url;
});

stopBtn.addEventListener("click", async () => {
  if (isRunning) {
    
    const res = await fetch("http://127.0.0.1:5000/stop_calculations", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
    });
    modalText.innerText = "Zatrzymano algorytm. Możesz go wznowić klikając poniższy guzik.";
    stopBtn.innerText = "Wznów obliczenia";
  }
  else {

    const res = await fetch("http://127.0.0.1:5000/continue_calculations", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
    });
    modalText.innerText = "Obliczenia trwają. Możesz zatrzymać je klikając poniższy guzik.";
    stopBtn.innerText = "Zatrzymaj obliczenia";

  }
    isRunning = !isRunning;
});

setInterval(() => {
    if (isRunning && isModalOpen) {
        time += 1;
        timerElement.innerText = 'Czas trwania obliczeń: ' + time + 's';
    }   
}, 1000);
