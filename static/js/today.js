const date = new Date();
const day = date.getDate();
const month = date.getMonth() + 1;
const year = date.getFullYear();

document.getElementById("today").innerText = `Dia: ${day.toString().padStart(2, "0")}/${month.toString().padStart(2, "0")}/${year}`;