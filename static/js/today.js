const hoje = new Date();
const dia = hoje.getDate();
const mes = hoje.getMonth() + 1;
const ano = hoje.getFullYear();
document.getElementById("hoje").innerText = `Data: ${dia.toString().padStart(2, "0")}/${mes.toString().padStart(2, "0")}/${ano}`;
