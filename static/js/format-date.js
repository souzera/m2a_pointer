function formatDate(element_id, date=new Date()) {
  const dia = date.getDate();
  const mes = date.getMonth() + 1;
  const ano = date.getFullYear();

  document.getElementById(element_id).innerText = `Data: ${dia
    .toString()
    .padStart(2, "0")}/${mes.toString().padStart(2, "0")}/${ano}`;
}


document.getElementById("date").innerText = formatDate("selected-date");