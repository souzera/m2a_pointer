function navigateTo(url) {
    /**
     * [PT]
     * 
     * NavigateTo é uma função que redireciona o usuário para uma nova página.
     * 
     * @param {string} url - URL para onde o usuário será redirecionado.
     * @returns {void}
     * 
     * [EN]
     * 
     * NavigateTo is a function that redirects the user to a new page.
     * 
     * @param {string} url - URL to where the user will be redirected.
     * @returns {void}
     */
    window.location.href = url
}

document.getElementById('navigate-to-diario').addEventListener('click', () => navigateTo('/empresa/diario/'))