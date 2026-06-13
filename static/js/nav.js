document.addEventListener("DOMContentLoaded", () => {
    // Marca o link ativo na navegação com base no URL atual
    const currentPath = window.location.pathname;
    document.querySelectorAll('.main-nav a, .sidebar-nav a').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});
