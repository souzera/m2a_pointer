function formatDate(element_id, date=new Date()) {
  /**
   * [PT]
   * 
   * Formatar a data no padrão dd/mm/aaaa
   * 
   * @param {string} element_id - ID do elemento que receberá a data formatada
   * @param {Date} date - Data a ser formatada
   * 
   * @returns {string} - Data formatada
   * 
   * [EN]
   * 
   * Format the date in the pattern dd/mm/yyyy
   * 
   * @param {string} element_id - ID of the element that will receive the formatted date
   * @param {Date} date - Date to be formatted
   * 
   * @returns {string} - Formatted date
   */
  const dia = date.getDate();
  const mes = date.getMonth() + 1;
  const ano = date.getFullYear();

  document.getElementById(element_id).innerText = `Data: ${dia
    .toString()
    .padStart(2, "0")}/${mes.toString().padStart(2, "0")}/${ano}`;
}


document.getElementById("date").innerText = formatDate("selected-date");