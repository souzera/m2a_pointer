function navigateTo(url) {
    window.location.href = url
}

document.getElementById('navigate-to-diario').addEventListener('click', () => navigateTo('/empresa/diario/'))