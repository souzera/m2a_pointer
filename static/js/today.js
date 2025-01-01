const hoje = new Date();
const dia = hoje.getDate();
const mes = hoje.getMonth() + 1;
const ano = hoje.getFullYear();
document.getElementById("hoje").innerText = `Data: ${dia}/${mes}/${ano}`;
