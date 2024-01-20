import { testFunctions, algorithms } from "./consts.js";

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

function createBox(label, parentNode, id, inputName) {
  const box = document.createElement("div");
  box.classList.add("box");
  const labelNode = document.createElement("p");
  labelNode.innerText = label;

  const inputDiv = document.createElement("div");
  inputDiv.classList.add("input-div");

  const input = document.createElement("input");
  input.type = "number";
  input.dataset.id = id;
  input.dataset.name = inputName;

  inputDiv.appendChild(input);
  box.appendChild(labelNode);
  box.appendChild(inputDiv);
  parentNode.appendChild(box);
}

function createFunctionSection(f) {
  const functionsSection =
    document.getElementsByClassName("functions-section")[0];

  const label = document.createElement("p");
  label.innerText = f.name;

  const functionInfo = document.createElement("div");
  functionInfo.classList.add("function-info");

  createBox("Wybierz dziedzinę", functionInfo, f.id, "domain");
  createBox("Wybierz wymiar", functionInfo, f.id, "dimension");

  functionsSection.appendChild(label);
  functionsSection.appendChild(functionInfo);
}

function createAlgorithmSection(a) {
  const algorithmsSection =
    document.getElementsByClassName("algorithms-section")[0];

  const label = document.createElement("p");
  label.innerText = a.name;

  const algorithmInfo = document.createElement("div");
  algorithmInfo.classList.add("algorithm-info");

  createBox(
    "Wybierz liczbę iteracji",
    algorithmInfo,
    a.id,
    "numberOfIterations",
  );
  createBox("Wybierz rozmiar populacji", algorithmInfo, a.id, "population");

  algorithmsSection.appendChild(label);
  algorithmsSection.appendChild(algorithmInfo);
}

const submitButton = document.getElementById("submit-btn");
const modal = document.getElementById("reportStateModal");
const pauseBtn = document.getElementById("pauseBtn");
const timerElement = document.getElementById("timer");
const modalText = document.getElementById("modalText");

let isRunning = true;
let isModalOpen = false;
let time = 0;

submitButton.addEventListener("click", async () => {
  modal.style.display = "block";
  isModalOpen = true;
  const functionsSection =
    document.getElementsByClassName("functions-section")[0];
  const functionsInfo =
    functionsSection.getElementsByClassName("function-info");
  const functionsDetails = [];
  for (const info of functionsInfo) {
    const inputs = info.getElementsByTagName("input");
    const functionDetail = {};
    for (const input of inputs) {
      functionDetail["id"] = input.dataset.id;
      if (input.dataset.name === "domain") {
        functionDetail["domain"] = Number(input.value);
      } else {
        functionDetail["dimension"] = Number(input.value);
      }
    }
    functionsDetails.push(functionDetail);
  }
  const algorithmsDetails = [];
  const algorithmsSection =
    document.getElementsByClassName("algorithms-section")[0];
  const algorithmsInfo =
    algorithmsSection.getElementsByClassName("algorithm-info");
  for (const info of algorithmsInfo) {
    const inputs = info.getElementsByTagName("input");
    const algorithmDetail = {};
    for (const input of inputs) {
      algorithmDetail["id"] = input.dataset.id;
      if (input.dataset.name === "numberOfIterations") {
        algorithmDetail["numberOfIterations"] = Number(input.value);
      } else {
        algorithmDetail["population"] = Number(input.value);
      }
    }
    algorithmsDetails.push(algorithmDetail);
  }
  console.log(functionsDetails);
  console.log(algorithmsDetails);

  const res = await fetch("http://127.0.0.1:5000/generate_text_report", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      functionsDetails,
      // Filter algorithms, because now we only support GOA algorithm
      algorithmsDetails: algorithmsDetails.filter((a) => a.id === "0"),
    }),
  });

  if (!res.ok) {
    throw new Error("Error while setting details");
  }

  const data = await res.json();
  console.log(data);
  const html = generateHTML(data);
  const blob = new Blob([html], { type: "text/html" });
  const url = URL.createObjectURL(blob);
  window.location.href = url;
});

pauseBtn.addEventListener("click", async () => {
  if (isRunning) {
    const res = await fetch("http://127.0.0.1:5000/pause_calculations", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    modalText.innerText =
      "Zatrzymano algorytm. Możesz go wznowić klikając poniższy guzik.";
    pauseBtn.innerText = "Wznów obliczenia";
  } else {
    const res = await fetch("http://127.0.0.1:5000/continue_calculations", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    modalText.innerText =
      "Obliczenia trwają. Możesz zatrzymać je klikając poniższy guzik.";
    pauseBtn.innerText = "Zatrzymaj obliczenia";
  }
  isRunning = !isRunning;
});

setInterval(() => {
  if (isRunning && isModalOpen) {
    time += 1;
    timerElement.innerText = "Czas trwania obliczeń: " + time + "s";
  }
}, 1000);

// Pewnie da sie jakoś sharować ten stan miedzy redirectem, ale mam już dość XD
document.addEventListener(
  "DOMContentLoaded",
  async () => {
    const res = await fetch(
      "http://127.0.0.1:5000/get_function_and_algorithm",
      {
        headers: {
          "Content-Type": "application/json",
        },
      },
    );
    const data = await res.json();
    const functionIds = data["functionIds"];
    const algorithmIds = data["algorithmIds"];
    for (const id of functionIds) {
      createFunctionSection(testFunctions[id]);
    }
    for (const id of algorithmIds) {
      createAlgorithmSection(algorithms[id]);
    }
  },
  false,
);
